# Agent Development Guide

This guide outlines how to create new agent types for Mimir.

1. **Create a Class**
   - Inherit from `AgenteBase` or an existing subtype.
   - Implement the `procesar_ciclo` method to define agent behavior.

2. **Place the File**
   - Add the new module inside `ecosistema_ia/agentes/tipos/` or a plugin directory.
   - Modules placed under `ecosistema_ia/plugins/` are automatically discovered.

3. **Test the Agent**
   - Write unit tests in `tests/` to validate core logic.
   - Run `pytest` to ensure the ecosystem loads your new type correctly.

By following these steps you can expand the ecosystem with minimal manual configuration.
