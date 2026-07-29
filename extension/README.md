# Chrome extension 2.0.0.20

## Восстановление готового ZIP

После **Code → Download ZIP** и распаковки репозитория выполни в PowerShell из корня папки:

```powershell
powershell -ExecutionPolicy Bypass -File tools/materialize-extension.ps1
```

Скрипт проверяет SHA-256 и создаёт:

```text
extension/release/business-bridge-chatgpt-extension-v2.0.0.20-autorun-ui-hidden.zip
extension/unpacked/
```

Ожидаемый SHA-256 ZIP:

```text
0a21193e3bde3e9e0b6adb76eb516f2fbc9db2b84137419812a969f2e2e8ba92
```

## Установка

1. Открой `chrome://extensions`.
2. Включи «Режим разработчика».
3. Нажми «Загрузить распакованное расширение».
4. Выбери папку `extension/unpacked`, внутри которой непосредственно лежит `manifest.json`.
5. Закрепи Business Bridge 2 на панели Chrome.
6. Обнови вкладку ChatGPT.

## Режим работы

Кнопка `▶ Авторежим` скрыта только визуально. Сборка рассчитана на ручной сценарий:

1. привязать диалог к Bridge-профилю;
2. выбрать CLI;
3. включить «Ручной режим writing blocks»;
4. нажать локальную Copy-кнопку внутри нужного code/writing block;
5. расширение одновременно сохраняет обычное копирование и отправляет точный блок в Bridge.

## Обновление unpacked-расширения

Для сохранения Chrome storage заменяй файлы **в той же папке**, затем нажимай Reload на существующей карточке расширения. При переносе в другую папку заранее используй «Экспортировать» в popup; экспорт содержит tokens и должен храниться как секрет.
