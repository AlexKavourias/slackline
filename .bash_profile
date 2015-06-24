alias cdauto="cd ~/git/eng/auto/bin/ && . ./env-setup.sh" 
alias wumbo="AUTO_PARAMETERS=akavourias-02"
alias bash="vi ~/.bash_profile"
alias mvm_ip="ManagementVm.py find keys=ipaddress"
alias googless="cd ~/git/eng/auto/lib/python/auto/testcase/googlesheet"
alias perf="cd ~/git/eng/auto/testcases/performance"
alias gs="git status"
ap () {
    if [ -z "$1" ]
    then
        echo "AUTO_PARAMETERS=$AUTO_PARAMETERS"
        return 0
    fi
    if [ "$1" == "pop" ]
    then
        export AUTO_PARAMETERS=$(echo $AUTO_PARAMETERS | awk -F, '{for (i=0;++i<=NF-1;)printf $i","}' | sed 's/,$//')
        #export AUTO_PARAMETERS=$(echo $AUTO_PARAMETERS | sed -e s/,[^,]*$//)
        return 0
    fi
    export AUTO_PARAMETERS=$1
    echo "AUTO_PARAMETERS=$AUTO_PARAMETERS"
}

aap()
{
    if [ -z "$1" ]
    then
        ap
    else
        tmpap=$(echo "${AUTO_PARAMETERS},$1")
        ap $tmpap
    fi
}

testbed()
{
    if [ -z "$1" ]
    then
        echo "testbed: requires a single argument"
    else
        python ~/git/eng/auto/bin/VcenterVm.py name=$1 show
    fi
}

lol() {
exec 1> >(lolcat); 
}

unlol() {
exec 1> /dev/stdout;
}
alias vimrc='vi ~/.vimrc'
alias dev='ssh ubuntu@akavourias-dev.infinio.com  -o SendEnv=AUTO_PARAMETERS'
alias grep="grep --color=auto"

source ~/git/eng/auto/bin/env-setup.sh
export PYTHONSTARTUP=~/pystart.py
