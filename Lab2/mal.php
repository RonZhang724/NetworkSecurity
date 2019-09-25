<?php

$cwd = getcwd();
print_r($cwd);

$files = scandir($cwd);
print_r($files);

$files = scandir('/');
print_r($files);

$output = shell_exec("ps aux --no-headers | wc -l");
print_r($output);
