import xml.etree.ElementTree as ET
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.parser.util import xpath_eval


class BPMNValidator(object):
    def __init__(self, xml, forms, userTasks):
        self.bpmn = {}
        self.xml = xml
        self.bpmnXML = ET.fromstring(self.xml)
        self.proccessXML = self.bpmnXML[len(self.bpmnXML) - 2]
        self.processXPath = xpath_eval(self.proccessXML)

        self.forms = forms
        self.userTask = userTasks
        self.allErrors = []

    def validate(self):
        self.validateDiagram()
        self.validatePerformers()
        return self.allErrors

    def validatePerformers(self):
        self._performers_all_tasks()

    def validateDiagram(self):
        self._diagram_pool()
        self._diagram_start_events()
        self._diagram_end_events()
        self._diagram_exclusive_gateway()
        self._diagram_task()
        self._diagram_manual_task()
        self._diagram_user_task()

    def _performers_all_tasks(self):
        ERRORPerformer = 'شما شخصی را برای انجام این مرحله انتخاب نکرده اید'
        allTasksIds = []
        for catch_event in self.processXPath('.//bpmn:task'):
            allTasksIds.append(catch_event.get('id'))
        for catch_event in self.processXPath('.//bpmn:userTask'):
            allTasksIds.append(catch_event.get('id'))
        for itm in self.userTask:
            if itm['taskId'] in allTasksIds:
                allTasksIds.remove(itm['taskId'])
        if len(allTasksIds) != 0:
            for itm in allTasksIds:
                self.allErrors.append(
                    self.errorDictMaker('performer', itm, 'task', ERRORPerformer))

    def _diagram_pool(self):
        ERROROnePool = 'هر فرایند حداکثر یک فضای فرایند می تواند داشته باشد.'
        if len(self.bpmnXML) != 3 and len(self.bpmnXML) != 2:
            self.allErrors.append(self.errorDictMaker('Pool', message=ERROROnePool))
        return self.allErrors

    def _diagram_start_events(self):
        ERRORName = 'برای این شکل باید نام وارد شود.'
        ERRORLeastOne = 'فرایند باید حداقل یک شروع داشته باشد.'
        ERROROutJust = 'به این شکل خطی نباید وارد شود.'
        ERRORInJust = 'از این شکل باید فقط یک خط خارج شود.'
        if not self.processXPath('.//bpmn:startEvent'):
            self.allErrors.append(self.errorDictMaker('StartEvent', message=ERRORLeastOne))
        else:
            for catch_event in self.processXPath('.//bpmn:startEvent'):
                itmName = catch_event.get('name')
                itmId = catch_event.get('id')
                if not itmName:
                    itmName = '?'
                    self.allErrors.append(self.errorDictMaker('StartEvent', itmId, itmName, ERRORName))
                incoming = self.processXPath('.//bpmn:sequenceFlow[@targetRef="%s"]' % itmId)
                if incoming:
                    self.allErrors.append(self.errorDictMaker('StartEvent', itmId, itmName, ERRORInJust))
                outgoing = self.processXPath('.//bpmn:sequenceFlow[@sourceRef="%s"]' % itmId)
                if not outgoing or len(outgoing) != 1:
                    self.allErrors.append(self.errorDictMaker('StartEvent', itmId, itmName, ERROROutJust))
        return self.allErrors

    def _diagram_end_events(self):
        ERRORName = 'برای این شکل باید نام وارد شود.'
        ERRORLeastOne = 'فرایند باید حداقل یک پایان داشته باشد.'
        ERROROutJust = 'از این شکل خطی نباید خارج شود.'
        ERRORInJust = 'به این شکل فقط باید یک خط وارد شود.'
        if not self.processXPath('.//bpmn:endEvent'):
            self.allErrors.append(self.errorDictMaker('endEvent', message=ERRORLeastOne))
        else:
            for catch_event in self.processXPath('.//bpmn:endEvent'):
                itmName = catch_event.get('name')
                itmId = catch_event.get('id')
                if not itmName:
                    itmName = '?'
                    self.allErrors.append(self.errorDictMaker('endEvent', itmId, itmName, ERRORName))
                incoming = self.processXPath('.//bpmn:sequenceFlow[@targetRef="%s"]' % itmId)
                if (not incoming) or (len(incoming) != 1):
                    self.allErrors.append(self.errorDictMaker('endEvent', itmId, itmName,
                                                              ERRORInJust))
                outgoing = self.processXPath('.//bpmn:sequenceFlow[@sourceRef="%s"]' % itmId)
                if outgoing:
                    self.allErrors.append(self.errorDictMaker('endEvent', itmId, itmName, ERROROutJust))
        return self.allErrors

    def _diagram_exclusive_gateway(self):
        ERRORName = 'برای این شکل باید نام وارد شود.'
        ERRORCondition = 'لطفا برای جداکننده قوانین را تعریف کنید.'
        ERROROutLeast = 'از این شکل حداقل باید یک خط خارج شود.'
        ERRORInLeast = 'به این شکل حداقل باید یک خط وارد شود.'

        for catch_event in self.processXPath('.//bpmn:exclusiveGateway'):
            itmName = catch_event.get('name')
            itmId = catch_event.get('id')
            itmType = 'exclusiveGateway'
            if not itmName:
                itmName = '?'
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERRORName))
            incoming = self.processXPath('.//bpmn:sequenceFlow[@targetRef="%s"]' % catch_event.get('id'))
            if not incoming:
                self.allErrors.append(
                    self.errorDictMaker(itmType, itmId, itmName, ERRORInLeast))

            outgoing = self.processXPath('.//bpmn:sequenceFlow[@sourceRef="%s"]' % catch_event.get('id'))

            if not outgoing:
                self.allErrors.append(
                    self.errorDictMaker(itmType, itmId, itmName, ERROROutLeast))
            else:
                if len(outgoing) > 1:
                    for itmSeq in outgoing:
                        seqId = itmSeq.get('id')
                        seqName = itmSeq.get('name')
                        seqType = 'sequenceFlow'
                        if not seqName:
                            self.allErrors.append(
                                self.errorDictMaker(seqType, seqId, seqName, ERRORName))
                        if len(itmSeq) == 1:
                            if not itmSeq[0].text or itmSeq[0].text == '' or itmSeq[0].text == ' ':
                                self.allErrors.append(
                                    self.errorDictMaker(itmType, itmId, itmName, ERRORCondition))
                        else:
                            self.allErrors.append(
                                self.errorDictMaker(itmType, itmId, itmName, ERRORCondition))
        return self.allErrors

    def _diagram_task(self):
        ERRORName = 'برای این شکل باید نام وارد شود.'
        ERROROutJust = 'از این شکل فقط باید یک خط خارج شود.'
        ERRORInJust = 'به این شکل فقط باید یک خط وارد شود.'
        for catch_event in self.processXPath('.//bpmn:task'):
            itmName = catch_event.get('name')
            itmId = catch_event.get('id')
            itmType = 'task'
            if not itmName:
                itmName = '?'
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERRORName))
            incoming = self.processXPath('.//bpmn:sequenceFlow[@targetRef="%s"]' % catch_event.get('id'))
            if not incoming:
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERRORInJust))

            outgoing = self.processXPath('.//bpmn:sequenceFlow[@sourceRef="%s"]' % catch_event.get('id'))
            if not outgoing or len(outgoing) != 1:
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERROROutJust))
        return self.allErrors

    def _diagram_manual_task(self):
        ERRORName = 'برای این شکل باید نام وارد شود.'
        ERROROutJust = 'از این شکل فقط باید یک خط خارج شود.'
        ERRORInJust = 'به این شکل فقط باید یک خط وارد شود.'
        for catch_event in self.processXPath('.//bpmn:manualTask'):
            itmName = catch_event.get('name')
            itmId = catch_event.get('id')
            itmType = 'manualTask'
            if not itmName:
                itmName = '?'
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERRORName))
            incoming = self.processXPath('.//bpmn:sequenceFlow[@targetRef="%s"]' % catch_event.get('id'))
            if not incoming:
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERRORInJust))

            outgoing = self.processXPath('.//bpmn:sequenceFlow[@sourceRef="%s"]' % catch_event.get('id'))
            if not outgoing or len(outgoing) != 1:
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERROROutJust))
        return self.allErrors

    def _diagram_user_task(self):
        ERRORName = 'برای این شکل باید نام وارد شود.'
        ERROROutJust = 'از این شکل فقط باید یک خط خارج شود.'
        ERROROneUserLeast = 'هر فرایند باید حداقل یک مرحله کاربری داشته باشد.'
        ERRORInJust = 'به این شکل فقط باید یک خط وارد شود.'
        flgAtleatsOne = 1
        for catch_event in self.processXPath('.//bpmn:userTask'):
            flgAtleatsOne = 0
            itmName = catch_event.get('name')
            itmId = catch_event.get('id')
            itmType = 'userTask'
            if not itmName:
                itmName = '?'
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERRORName))
            incoming = self.processXPath('.//bpmn:sequenceFlow[@targetRef="%s"]' % catch_event.get('id'))
            if not incoming:
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERRORInJust))

            outgoing = self.processXPath('.//bpmn:sequenceFlow[@sourceRef="%s"]' % catch_event.get('id'))
            if not outgoing or len(outgoing) != 1:
                self.allErrors.append(self.errorDictMaker(itmType, itmId, itmName, ERROROutJust))
        if flgAtleatsOne:
            self.allErrors.append(self.errorDictMaker('userTask', message=ERROROneUserLeast))
        return self.allErrors

    def errorDictMaker(self, type='', id='', name='', message='please call taraan support'):
        return {'type': type, 'id': id, 'name': name, 'message': message}