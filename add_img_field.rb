File.readlines(ARGV[0]).each do |line|
  fields = line.chomp.split(/\t/)
  fields.push %!<img src="google-img--#{fields[0]}.jpg">!
  puts fields.join("\t")
end
