package com.stocktracker.stock_tracker_scheduler.scheduler;

import org.quartz.JobBuilder;
import org.quartz.JobDetail;
import org.quartz.SimpleScheduleBuilder;
import org.quartz.Trigger;
import org.quartz.TriggerBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class QuartzSchedulerConfig {

    @Bean
    public JobDetail pythonJobDetail() {
        return JobBuilder.newJob(PythonJob.class)
                .withIdentity("pythonJob")
                .storeDurably()
                .build();
    }

    @Bean
    public Trigger pythonJobTrigger(JobDetail pythonJobDetail) {
        return TriggerBuilder.newTrigger()
                .forJob(pythonJobDetail)
                .withIdentity("pythonJobTrigger")

                .withSchedule(SimpleScheduleBuilder.simpleSchedule()
                        .withIntervalInSeconds(10)
                        .repeatForever())
                        
                .startNow()
                
                .build();
    }
}
