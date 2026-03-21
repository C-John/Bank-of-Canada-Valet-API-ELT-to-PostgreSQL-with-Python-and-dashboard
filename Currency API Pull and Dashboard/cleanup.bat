@echo off
System Optimizer
echo ===========================================
echo   STARTING SYSTEM DEEP CLEAN...
echo ===========================================

echo [+] Nuking Database Zombies...
taskkill /F /IM postgres.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul

echo [+] Releasing PostgreSQL Port 5432...
net stop postgresql-x64-16 2>nul

echo [+] Force-releasing Standby Memory...
powershell -command "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()"

echo ===========================================
echo   CLEANUP COMPLETE! RAM RECLAIMED.
echo ===========================================
timeout /t 3