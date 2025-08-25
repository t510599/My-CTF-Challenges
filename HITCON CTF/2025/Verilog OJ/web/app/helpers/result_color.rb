# frozen_string_literal: true

def result_color(result) # rubocop:disable Metrics/MethodLength
  case result
  when 'AC'
    'green'
  when 'WA'
    'red'
  when 'TLE'
    'blue'
  when 'RE'
    'purple'
  when 'R'
    'black'
  else
    'gray'
  end
end
