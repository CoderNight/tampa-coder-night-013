require 'bundler/setup'

def root(*path)
  File.join(File.expand_path("../..", __FILE__), path)
end

def fixture(*path)
  root('spec/fixtures', path)
end
