package com.stocktracker.stock_tracker_scheduler.controller;

import org.quartz.JobDetail;
import org.quartz.Scheduler;
import org.quartz.SchedulerException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/scheduler")
public class SchedulerController {

    @Autowired
    private Scheduler scheduler;

    @Autowired
    private JobDetail pythonJobDetail;

    @PostMapping("/trigger-python-job")
    public String triggerPythonJob() throws SchedulerException {
        try {
            scheduler.triggerJob(pythonJobDetail.getKey());
            return "Python job triggered successfully!";
        } catch (Exception e) {
            e.printStackTrace();
            return "Failed to trigger Python job: " + e.getMessage();
        }
    }
}
