# Example project tree, not a scaffold

All product and package identifiers in this illustration are fictional. HarborDesk is an invented application; harbor_desk is its invented Python module. The tree illustrates responsibilities, not a required architecture or evidence of ideal layering. Do not expose source-project names, customer names, internal hostnames or repository identifiers when creating reusable examples. Use the actual inspected project's paths only in that project's requested review/design/plan, where they are needed as evidence.

```text
HarborDesk/
├── apps/
│   ├── api/                  HTTP entry
│   └── worker/               Background entry
├── backend/
│   ├── src/harbor_desk/
│   │   ├── core/             Shared foundations/configuration
│   │   ├── database/         ORM/data access
│   │   ├── domain/           Domain types/rules
│   │   ├── integrations/     External systems
│   │   └── services/         Application operations
│   ├── alembic/
│   ├── assets/
│   ├── scripts/
│   └── tests/
├── frontend/
│   ├── src/{app,features,pages,shared,test}/
│   ├── public/
│   └── scripts/
├── contracts/
├── deploy/
├── ci/
├── tests/
├── scripts/
└── docs/
```

Before proposing a tree: identify domain responsibilities with [domain discovery](domain-discovery.md), decide interaction boundaries with [context relationships](context-relationships.md), and choose a suitable [architecture style](architecture-patterns.md). Show why each proposed directory exists, who may depend on it and where its public contract lives. Existing justified structures take precedence over resemblance to this tree. Do not create empty layers or impose a web layout on desktop/CLI tools. Adapting another project does not rewrite the source specification.
