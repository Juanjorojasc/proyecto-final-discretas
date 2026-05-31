@echo off
REM this only works on windows. If you are on linux, then you probably already know 
REM how to implement something like this.

setlocal enabledelayedexpansion

for /l %%i in (1, 1, 5) do (
    echo _____________ Iteration %%i with input file "in_0%%i.txt" and compare file "ou_0%%i.txt"_____________

    python main.py -read_case=cases\in_0%%i.txt -print_cmp=my_ans.txt


    fc my_ans.txt cases\ou_0%%i.txt > nul || goto :bad
)

echo All was ok :)
goto :out

:bad
echo Something was wrong....

:out
del my_ans.txt
echo on