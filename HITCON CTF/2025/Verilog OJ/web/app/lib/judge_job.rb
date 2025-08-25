# frozen_string_literal: true

require 'sidekiq'
require_relative '../models/submission'

module VerilogOJ
  # Judge Job
  class JudgeJob
    include Sidekiq::Job

    def perform(submission_id)
      submission = Submission.first(id: submission_id)
      return if submission.nil? || submission.result != 'Q'

      dir = prepare(submission)
      result, output = judge dir
      submission.update(result: result, output: output) unless result.nil?
      FileUtils.remove_dir(dir, force: true)
    end

    def prepare(submission)
      dir = Dir.mktmpdir("submission_#{submission.id}_")
      File.write("#{dir}/testbench.v", submission.problem.testbench)
      File.write("#{dir}/module.v", submission.code)
      dir
    end

    def judge(dir) # rubocop:disable Metrics/MethodLength
      stdout, stderr, status = Timeout.timeout(15) do
        # To simply error handling, let iverilog and vvp fail in a single script
        script_path = File.realpath("#{File.dirname(__FILE__)}/../../scripts/judge.sh")
        # iverilog is safe to execute
        Open3.capture3("#{script_path} #{dir}")
      end

      return ['RE', stderr] unless status.exitstatus.zero?

      if !stdout.nil? && stdout.strip.lines.last == 'Passed'
        ['AC', stdout]
      else
        ['WA', stdout]
      end
    rescue Timeout::Error
      ['TLE', 'Execution timed out']
    rescue StandardError => e
      ['RE', e.message]
    end
  end
end
