import zipfile
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.storage.Packager import Packager
import xml.etree.ElementTree as ET

class MyPackager(Packager):
    def create_package_xml(self):
        """
        Creates the package, writing the data out to the provided file-like object.
        """
        self.bpmn = {}
        for bpmn in self.input_files:
            self.parser.add_bpmn_xml(bpmn)
        self.wf_spec = self.parser.get_spec(self.entry_point_process)

        self.package_zip = zipfile.ZipFile(self.package_file, "w", compression=zipfile.ZIP_DEFLATED)

        done_files = set()
        # for spec in self.wf_spec.get_specs_depth_first():
        filename = self.wf_spec.file
        if not filename in done_files:
            for bpmn in self.input_files:
                done_files.add(filename)
                self.write_to_package_zip("%s.bpmn" % self.wf_spec.name, ET.tostring(bpmn))
                # self.write_file_to_package_zip("src/" + self._get_zip_path(filename), filename)
                self._call_editor_hook('package_for_editor', self.wf_spec, filename)

        self.write_meta_data()
        self.write_manifest()
        self.package_zip.close()