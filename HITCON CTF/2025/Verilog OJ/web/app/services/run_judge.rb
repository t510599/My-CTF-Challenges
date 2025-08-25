# frozen_string_literal: true

require_relative '../models/problem'
require_relative '../models/submission'
require_relative '../lib/judge_job'

module VerilogOJ
  # Judge Service
  class RunJudgeService
    def call(problem_id, code)
      submission = Submission.create(problem_id: problem_id, code: code, result: 'Q')

      JudgeJob.perform_async(submission.id)
    end
  end
end
