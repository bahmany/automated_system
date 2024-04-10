var g = new JSGantt.GanttChart(document.getElementById('embedded-Gantt'), 'week');

var faLang =
    {
        'format': 'فرمت',
        'hour': 'ساعت',
        'day': 'روز',
        'week': 'هفته',
        'month': 'ماه',
        'quarter': 'ربع',
        'hours': 'ساعات',
        'days': 'روزها',
        'weeks': 'هفته ها',
        'months': 'ماه ها',
        'quarters': 'ربع ها',
        'hr': 'س',
        'dy': 'روز',
        'wk': 'هفته',
        'mth': 'ماه',
        'qtr': 'ر',
        'hrs': 'س',
        'dys': 'روزها',
        'wks': 'هفته ها',
        'mths': 'ماهها',
        'qtrs': 'ربع ها',
        'resource': 'منبع',
        'duration': 'دوره',
        'comp': '% تکمیل.',
        'completion': 'تکمیل',
        'startdate': 'تاریخ شروع',
        'enddate': 'تاریخ پایان',
        'moreinfo': 'اطلاعات بیشتر',
        'notes': 'یادداشت ها',
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'maylong': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'november': 'November',
        'december': 'December',
        'jan': 'Jan',
        'feb': 'Feb',
        'mar': 'Mar',
        'apr': 'Apr',
        'may': 'May',
        'jun': 'Jun',
        'jul': 'Jul',
        'aug': 'Aug',
        'sep': 'Sep',
        'oct': 'Oct',
        'nov': 'Nov',
        'dec': 'Dec',
        'sunday': 'Sunday',
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sun': 'Sun',
        'mon': 'Mon',
        'tue': 'Tue',
        'wed': 'Wed',
        'thu': 'Thu',
        'fri': 'Fri',
        'sat': 'Sat'
    }


g.addLang("fa",faLang);

g.setLang("fa");
if (g.getDivId() != null) {
    g.setCaptionType('Complete');  // Set to Show Caption (None,Caption,Resource,Duration,Complete)
    g.setQuarterColWidth(36);
    g.setDateTaskDisplayFormat('day dd month yyyy'); // Shown in tool tip box
    g.setDayMajorDateDisplayFormat('mon yyyy - Week ww') // Set format to display dates in the "Major" header of the "Day" view
    g.setWeekMinorDateDisplayFormat('dd mon') // Set format to display dates in the "Minor" header of the "Week" view
    g.setShowTaskInfoLink(1); // Show link in tool tip (0/1)
    g.setShowEndWeekDate(0); // Show/Hide the date for the last day of the week in header for daily view (1/0)
    g.setUseSingleCell(10000); // Set the threshold at which we will only use one cell per table row (0 disables).  Helps with rendering performance for large charts.
    g.setFormatArr('Day', 'Week', 'Month', 'Quarter'); // Even with setUseSingleCell using Hour format on such a large chart can cause issues in some browsers
    // Parameters                     (pID, pName,                  pStart,       pEnd,        pStyle,         pLink (unused)  pMile, pRes,       pComp, pGroup, pParent, pOpen, pDepend, pCaption, pNotes, pGantt)
    g.AddTaskItem(new JSGantt.TaskItem(1, 'Define Chart API', '', '', 'ggroupblack', '', 0, 'Brian', 0, 1, 0, 1, '', '', 'Some Notes text', g));
    g.AddTaskItem(new JSGantt.TaskItem(11, 'Chart Object', '2017-02-20', '2017-02-20', 'gmilestone', '', 1, 'Shlomy', 100, 0, 1, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(12, 'Task Objects', '', '', 'ggroupblack', '', 0, 'Shlomy', 40, 1, 1, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(121, 'Constructor Proc', '2017-02-21', '2017-03-09', 'gtaskblue', '', 0, 'Brian T.', 60, 0, 12, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(122, 'Task Variables', '2017-03-06', '2017-03-11', 'gtaskred', '', 0, 'Brian', 60, 0, 12, 1, 121, '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(123, 'Task by Minute/Hour', '2017-03-09', '2017-03-14 12:00', 'gtaskyellow', '', 0, 'Ilan', 60, 0, 12, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(124, 'Task Functions', '2017-03-09', '2017-03-29', 'gtaskred', '', 0, 'Anyone', 60, 0, 12, 1, '123SS', 'This is a caption', null, g));
    g.AddTaskItem(new JSGantt.TaskItem(2, 'Create HTML Shell', '2017-03-24', '2017-03-24', 'gtaskyellow', '', 0, 'Brian', 20, 0, 0, 1, 122, '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(3, 'Code Javascript', '', '', 'ggroupblack', '', 0, 'Brian', 0, 1, 0, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(31, 'Define Variables', '2017-02-25', '2017-03-17', 'gtaskpurple', '', 0, 'Brian', 30, 0, 3, 1, '', 'Caption 1', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(32, 'Calculate Chart Size', '2017-03-15', '2017-03-24', 'gtaskgreen', '', 0, 'Shlomy', 40, 0, 3, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(33, 'Draw Task Items', '', '', 'ggroupblack', '', 0, 'Someone', 40, 2, 3, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(332, 'Task Label Table', '2017-03-06', '2017-03-09', 'gtaskblue', '', 0, 'Brian', 60, 0, 33, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(333, 'Task Scrolling Grid', '2017-03-11', '2017-03-20', 'gtaskblue', '', 0, 'Brian', 0, 0, 33, 1, '332', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(34, 'Draw Task Bars', '', '', 'ggroupblack', '', 0, 'Anybody', 60, 1, 3, 0, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(341, 'Loop each Task', '2017-03-26', '2017-04-11', 'gtaskred', '', 0, 'Brian', 60, 0, 34, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(342, 'Calculate Start/Stop', '2017-04-12', '2017-05-18', 'gtaskpink', '', 0, 'Brian', 60, 0, 34, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(343, 'Draw Task Div', '2017-05-13', '2017-05-17', 'gtaskred', '', 0, 'Brian', 60, 0, 34, 1, '', '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(344, 'Draw Completion Div', '2017-05-17', '2017-06-04', 'gtaskred', '', 0, 'Brian', 60, 0, 34, 1, "342,343", '', '', g));
    g.AddTaskItem(new JSGantt.TaskItem(35, 'Make Updates', '2017-07-17', '2017-09-04', 'gtaskpurple', '', 0, 'Brian', 30, 0, 3, 1, '333', '', '', g));

    g.Draw();
} else {
    alert("Error, unable to create Gantt Chart");
}


