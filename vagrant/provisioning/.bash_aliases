alias sshtorouter='ssh ubuntu@127.0.0.1 -p 2221'
alias sshtorouter2='ssh ubuntu@127.0.0.1 -p 2225'
alias sshtoc1='ssh ubuntu@127.0.0.1 -p 2222'
alias sshtoc2='ssh ubuntu@127.0.0.1 -p 2223'
alias sshtoswitch='ssh ubuntu@127.0.0.1 -p 2224'
alias sshtomininet='ssh mininet@127.0.0.1 -p 2226'
alias sshtoorchestrator='ssh ubuntu@127.0.0.1 -p 3333'
alias mypyfrmt='python ~/Programmieren/Python/mypyfilefrmt/mypyfilefrmt.py'
alias mydate='date "+%Y_%m_%d-%H_%M_%S"'
alias mydateiso='date "+%F %T"'
alias cdmininetscripts='cd /Users/Benny/Programmieren/SDN/SDNMininetScripts'
alias cduni='cd /Users/Benny/Documents/Uni/SS2017/Master/msc_vollmer_controller/msc-vollmer-distributed-controller'
alias cdsdn='cd ~/Programmieren/SDN/'


#VBOX


alias vbstartrouter='VBoxManage startvm "router" --type headless'
alias vbstartc1='VBoxManage startvm "controller1" --type headless'
alias vbstartc2='VBoxManage startvm "controller2" --type headless'
alias vbstartswitch='VBoxManage startvm "ofswitch" --type headless'


# Keynote
keynote_format_file(){
    highlight -O rtf $1 | pbcopy
    echo "Copied formatted file to clipboard!"
}
alias ll='ls -lha'
alias cduni='cd /Users/Benny/Documents/Uni/WS2016_2017'
#alias cdbsc='cd /Users/Benny/Documents/Uni/SS2015/Bsc/BachelorThesis'
alias cdfood='cd /Users/Benny/Programmieren/XCode/Bitbucket/AnAppleADay'
alias cdauk='cd /Users/Benny/Documents/Uni/WS2015_2016/Algokomplex/Aufgaben/auk'
alias cddb='cd /Users/Benny/Documents/Uni/SS2016/DB2/db2-superpowerforceultra'
alias cdct='cd /Users/Benny/Documents/Uni/SS2016/cT/codierungstheorie_kris'
alias cdcp='cd /Users/Benny/Documents/Uni/SS2016/computationalphotography'
alias cdwur='cd /Users/Benny/Documents/Uni/SS2016/WundR/uebungen_wahrscheinlichkeit_risiko'
alias settimer='python ~/Programmieren/Python/python_timer_for_mac_os/PyTimer/pytimer.py'
alias vprecho='python ~/Programmieren/Python/vprwvecho/vprwvecho.py'
alias gb='cd ..'
alias duh='du -hsx *'
alias gitadd='git add -A'
alias wisecow='fortune | cowsay'
alias runscip='/Users/Benny/Programmieren/SCIP/scipoptsuite-3.2.0/scip-3.2.0/bin/scip'
alias ipwlan='ifconfig | grep -A 6 en0 | grep "inet "'
alias lsusb='system_profiler SPUSBDataType'
#alias lanscan='arp-scan --localnet --numeric --ignoredups | grep -E "([a-f0-9]{2}:){5}[a-f0-9]{2}"'
alias airport='sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport'
#alias psql='/Applications/Postgres.app/Contents/Versions/9.5/bin/psql-p5432'
alias stata='/Applications/Stata/StataSE.app/Contents/MacOS/stata-se'
alias startmate='VBoxManage startvm MATE'
# read alias file
alias cdthesis='cd /Users/Benny/Documents/Uni/SS2017/Master/msc_vollmer_controller/msc-vollmer-distributed-controller/Thesis/BenjaminVollmerMA'

#stupid piece of garbage mac os ssh stuff:
ssh-add
#thanks steve ...

alias find_in_files='find . -type f -print0 | xargs -0 grep'
alias cddf='cd /Users/Benny/Programmieren/SDN/dragonflow'
# TODO new find in files
# grep -nr "$1" .

# Docker
alias docker-clear='docker rm -f $(docker ps -aq)'

