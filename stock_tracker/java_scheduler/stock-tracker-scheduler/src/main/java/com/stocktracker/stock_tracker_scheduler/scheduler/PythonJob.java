package com.stocktracker.stock_tracker_scheduler.scheduler;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

public class PythonJob implements Job {

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        System.out.println("🔹 Python job triggered by Quartz...");

        try {
            String pythonExe = System.getenv("PYTHON_EXE"); 
            if (pythonExe == null || pythonExe.isEmpty()) {
                pythonExe = "python"; // fallback to default in PATH
            }


            String projectDir = System.getProperty("user.dir"); 
            String scriptPath = projectDir + "\\stock_tracker\\tracker\\main.py";

            System.out.println("🔹 Executing: " + pythonExe + " " + scriptPath);

            ProcessBuilder processBuilder = new ProcessBuilder(pythonExe, scriptPath);
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream())
            );

            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("🐍 Python Output: " + line);
            }

            int exitCode = process.waitFor();
            System.out.println("✅ Python script finished with exit code: " + exitCode);

        } catch (Exception e) {
            System.err.println("❌ Error executing Python script:");
            e.printStackTrace();
        }
    }
}
