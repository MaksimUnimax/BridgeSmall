# SSH-туннель

Сервер слушает только `127.0.0.1:18083`. Расширение принимает только localhost endpoint, поэтому нужен SSH local forward.

## Windows PowerShell

```powershell
ssh -N -o ExitOnForwardFailure=yes -L 18083:127.0.0.1:18083 SSH_USER@SERVER_IP
```

Пример:

```powershell
ssh -N -o ExitOnForwardFailure=yes -L 18083:127.0.0.1:18083 root@80.74.29.249
```

При нестандартном SSH port:

```powershell
ssh -p SSH_PORT -N -o ExitOnForwardFailure=yes -L 18083:127.0.0.1:18083 SSH_USER@SERVER_IP
```

Окно PowerShell должно оставаться открытым.

## Если локальный port 18083 занят

Используй другой **локальный** port, не меняя сервер:

```powershell
ssh -N -o ExitOnForwardFailure=yes -L 28083:127.0.0.1:18083 SSH_USER@SERVER_IP
```

Тогда endpoint расширения:

```text
http://127.0.0.1:28083
```

## Локальная проверка

В другом PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:18083/v2/health
```

Ожидаются `ok`, `server_version`, `api_contract` и `request_id`.

## Завершение туннеля

Нажми `Ctrl+C` в окне, где запущен `ssh -N`. Это не останавливает серверный сервис.
