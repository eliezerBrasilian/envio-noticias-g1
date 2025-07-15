$action = New-ScheduledTaskAction -Execute 'python' -Argument "C:\Users\Eliezer\Documents\DEV\PYTHON\g1_requests\main.py"
$trigger1 = New-ScheduledTaskTrigger -Daily -At 08:30
$trigger2 = New-ScheduledTaskTrigger -Daily -At 15:00
$trigger3 = New-ScheduledTaskTrigger -Daily -At 18:00
$trigger4 = New-ScheduledTaskTrigger -Daily -At 22:00

Register-ScheduledTask -TaskName "g1-requests" -Action $action -Trigger @($trigger1, $trigger2, $trigger3, $trigger4) -Description "Envia noticias oficiais do g1 para o Telegram"
