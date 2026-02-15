# Skill Development Reference (from plugin-dev)

> Source: https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md

## Key Requirements

### Description (Frontmatter)
- Third-person: "This skill should be used when the user asks to..."
- Include specific trigger phrases
- Concrete scenarios

### Writing Style
- Imperative/infinitive form (verb-first)
- NOT second person
- Objective, instructional language

### Progressive Disclosure
1. Metadata (name + description) - Always in context (~100 words)
2. SKILL.md body - When skill triggers (<5k words, ideally 1,500-2,000)
3. Bundled resources - As needed (unlimited)

### Structure
```
skill-name/
├── SKILL.md (required, 1,500-2,000 words)
├── references/    - Documentation loaded as needed
├── templates/     - Template files for output
└── scripts/       - Executable utilities
```

### Validation Checklist
- [ ] SKILL.md with valid YAML frontmatter (name + description)
- [ ] Third-person description with trigger phrases
- [ ] Imperative/infinitive writing style
- [ ] Body 1,500-2,000 words (max 5k)
- [ ] Detailed content in references/
- [ ] All referenced files exist
- [ ] No duplicated information
