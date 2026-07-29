# BridgeSmall — Business Bridge 2

Этот репозиторий — единая точка входа для **ChatGPT и Codex**.

Он содержит:

- Chrome-расширение Business Bridge 2 `2.0.0.20`;
- сервер Business Bridge 2 `2.0.0-alpha.2`;
- автономный установщик серверной части для Codex;
- точную инструкцию по SSH-туннелю;
- пошаговый сценарий настройки расширения;
- acceptance-тест всей цепочки ChatGPT → расширение → сервер → CLI → ChatGPT;
- диагностику и rollback.

## Кто что делает

- **Codex на сервере** читает [`AGENTS.md`](AGENTS.md) и [`docs/CODEX_SERVER_DEPLOY_PROMPT.md`](docs/CODEX_SERVER_DEPLOY_PROMPT.md), проверяет сервер, устанавливает Bridge 2 и возвращает оператору параметры подключения.
- **ChatGPT** читает [`docs/CHATGPT_OPERATOR_GUIDE.md`](docs/CHATGPT_OPERATOR_GUIDE.md) и ведёт оператора пошагово.
- **Оператор** выполняет только действия, которые нельзя сделать удалённо: загружает unpacked-расширение в Chrome, держит SSH-туннель открытым, вводит локальный endpoint и token, включает ручной режим и нажимает локальную Copy-кнопку writing block.

## Быстрый маршрут

1. Передай Codex содержимое [`docs/CODEX_SERVER_DEPLOY_PROMPT.md`](docs/CODEX_SERVER_DEPLOY_PROMPT.md).
2. Скачай ZIP из [`extension/release/`](extension/release/) и установи его через `chrome://extensions` → «Режим разработчика» → «Загрузить распакованное расширение».
3. Создай SSH-туннель по [`docs/SSH_TUNNEL_GUIDE.md`](docs/SSH_TUNNEL_GUIDE.md).
4. Настрой Bridge-профиль по [`docs/CHATGPT_OPERATOR_GUIDE.md`](docs/CHATGPT_OPERATOR_GUIDE.md).
5. Пройди [`docs/ACCEPTANCE_TEST.md`](docs/ACCEPTANCE_TEST.md).

## Важное изменение расширения 2.0.0.20

Кнопка `▶ Авторежим` скрыта **только в UI**. Её DOM-элемент, обработчики, worker-маршруты, storage и серверная функциональность не удалены. Рабочий пользовательский сценарий этой сборки — **ручной режим writing blocks**.

## Проверенные тесты

- extension: `104 passed`, `0 failed`;
- server: `46 passed`, `0 failed`;
- серверный source snapshot SHA-256: `a84aaa9d98b9eaf706137813759d6d4a8430855894c7bcc017237837a7d925af`.

## Ограничения текущей серверной версии

- сервис работает от `root` в compatibility mode;
- один bearer token образует одну доверенную группу;
- prompt передаётся CLI через argv;
- listener обязан оставаться loopback-only;
- сервер нельзя публиковать напрямую в интернет — доступ только через SSH-туннель.
