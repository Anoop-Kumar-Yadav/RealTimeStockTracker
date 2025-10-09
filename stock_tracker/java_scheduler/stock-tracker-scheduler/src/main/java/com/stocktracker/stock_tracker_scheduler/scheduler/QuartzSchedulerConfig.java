package com.stocktracker.stock_tracker_scheduler.scheduler;

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
        return org.quartz.JobBuilder.newJob(PythonJob.class)
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
                        .withIntervalInSeconds(10)  // runs every 10 seconds
                        .repeatForever())
                .startNow()
                .build();
    }
}


// package com.stocktracker.stock_tracker_scheduler.scheduler;

// import org.quartz.CronScheduleBuilder;
// import org.quartz.CronTrigger;
// import org.quartz.JobDetail;
// import org.quartz.TriggerBuilder;
// import org.springframework.context.annotation.Bean;
// import org.springframework.context.annotation.Configuration;

// @Configuration
// public class QuartzSchedulerConfig {

//     @Bean
//     public JobDetail pythonJobDetail() {
//         return JobBuilder.newJob(PythonJob.class)
//                 .withIdentity("pythonJob")
//                 .storeDurably()
//                 .build();
//     }

//     @Bean
//     public CronTrigger pythonJobTrigger(JobDetail pythonJobDetail) {
//         return TriggerBuilder.newTrigger()
//                 .forJob(pythonJobDetail)
//                 .withIdentity("pythonJobCronTrigger")
//                 // Cron: 0 0 16 ? * MON-FRI -> 4:00 PM Mon-Fri
//                 .withSchedule(CronScheduleBuilder.cronSchedule("0 0 16 ? * MON-FRI"))
//                 .build();
//     }
// }
