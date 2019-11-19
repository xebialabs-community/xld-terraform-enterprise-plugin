SET JAVA_HOME=C:\app\jdk-8.0.232.09-hotspot
REM Get Java executable
if "%JAVA_HOME%"=="" (
  set JAVACMD=java
) else (
  set JAVACMD="%JAVA_HOME%\bin\java"
)

%JAVACMD% -jar C:\app\q\jython-standalone-2.7.1.jar C:\app\q\walk.py