package com.stocktracker.stock_tracker_scheduler;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class StockTrackerSchedulerApplication {

	public static void main(String[] args) {
		SpringApplication.run(StockTrackerSchedulerApplication.class, args);
		System.out.println("Spring Boot Stock Tracker Scheduler started!");
	}

}
