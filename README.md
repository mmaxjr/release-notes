# release-notes

CLI simples para gerar notas de versão a partir das mensagens de commit do Git.

## Uso

```text
python release_notes.py v1.0.0 v1.1.0 --title v1.1.0
python release_notes.py v1.0.0 v1.1.0 --kind feat --kind fix
python -m unittest -v
```

Commits no formato `feat:`, `fix:` e `docs:` são agrupados automaticamente.
Use `--kind` para limitar a saída a uma ou mais categorias.
