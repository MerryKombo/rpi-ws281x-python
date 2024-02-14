#!/bin/bash

while IFS= read -r line
do
  ip=$(echo $line | cut -d' ' -f1)
  ssh-copy-id -i /home/poddingue/.ssh/roundernetes.pub poddingue@$ip
done < <(grep -oP '^\d+\.\d+\.\d+\.\d+' inventory.ini)