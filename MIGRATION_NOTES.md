# Migration Notes

## Inventory

| Repo | Files | Locales | Total Keys |
| --- | ---: | --- | ---: |
| `adonis` | 14 | ar, de, en, es, fr, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 868 |
| `django` | 14 | ar, de, en, es, fr, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 1918 |
| `dotnet` | 10 | ar, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 380 |
| `filament` | 4 | de, en, es, fr | 1372 |
| `go` | 10 | ar, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 400 |
| `laravel` | 70 | ar, de, en, es, fr, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 2926 |
| `nestjs` | 10 | ar, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 380 |
| `phoenix` | 10 | ar, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 400 |
| `rails` | 14 | ar, de, en, es, fr, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 1260 |
| `spring` | 10 | ar, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 380 |
| `symfony` | 10 | ar, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 400 |
| `vue` | 14 | ar, de, en, es, fr, it, ja, ko, nl, pl, pt-BR, ru, tr, zh-CN | 8810 |
| `wordpress` | 14 | ar, de, es, fr, it, ja, ko, nl, pl, pt-BR, ru, template, tr, zh-CN | 6118 |

## Canonical Decisions

- Locale set normalized to `ar`, `de`, `en`, `es`, `fr`, `it`, `ja`, `ko`, `nl`, `pl`, `pt-BR`, `ru`, `tr`, and `zh-CN`.
- Placeholder syntax normalized to `{name}` across the canonical JSON files.
- Vue locale values win on conflicting shared keys. Remaining conflicts are resolved by source priority: Laravel, Filament, Rails, compact backend cluster, Django, then WordPress.
- Django gettext strings were consolidated under the `djangoStrings.*` namespace, using deterministic keys derived from the English `msgid` values.
- WordPress gettext strings were consolidated under the `wordpressStrings.*` namespace, using deterministic keys derived from the English POT catalog.

## Partial Locales

- `ar`: 346 keys fallback to English.
- `de`: 45 keys fallback to English.
- `es`: 45 keys fallback to English.
- `fr`: 45 keys fallback to English.
- `it`: 346 keys fallback to English.
- `ja`: 346 keys fallback to English.
- `ko`: 346 keys fallback to English.
- `nl`: 346 keys fallback to English.
- `pl`: 346 keys fallback to English.
- `pt-BR`: 346 keys fallback to English.
- `ru`: 346 keys fallback to English.
- `tr`: 346 keys fallback to English.
- `zh-CN`: 346 keys fallback to English.

## Divergences

### `ar`
- `status.reopened`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `status.reopened`: kept `vue` value over `nestjs`.
- `activity.statusChanged`: kept `vue` value over `nestjs`.
- `activity.assigned`: kept `vue` value over `nestjs`.
- `activity.unassigned`: kept `vue` value over `nestjs`.
- `activity.priorityChanged`: kept `vue` value over `nestjs`.
- `activity.tagAdded`: kept `vue` value over `nestjs`.
- `activity.tagRemoved`: kept `vue` value over `nestjs`.
- `activity.slaBreached`: kept `vue` value over `nestjs`.
- `activity.replied`: kept `vue` value over `nestjs`.
- `activity.noteAdded`: kept `vue` value over `nestjs`.
- `activity.departmentChanged`: kept `vue` value over `nestjs`.
- `ticket.created`: kept `vue` value over `nestjs`.
- Additional conflicts omitted: 65.

### `de`
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.macroApplied`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `ticket.macroApplied`: kept `laravel` value over `adonis`.
- `ticket.unfollowed`: kept `laravel` value over `adonis`.
- `ticket.notePinned`: kept `rails` value over `adonis`.
- `ticket.created`: kept `vue` value over `adonis`.
- `ticket.reopened`: kept `laravel` value over `adonis`.
- `middleware.notAgent`: kept `laravel` value over `adonis`.
- `inbound.disabled`: kept `rails` value over `adonis`.
- `status.reopened`: kept `vue` value over `adonis`.

### `en`
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `adonis`.
- `inbound.disabled`: kept `rails` value over `adonis`.

### `es`
- `status.inProgress`: kept `vue` value over `laravel`.
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `priority.low`: kept `vue` value over `laravel`.
- `priority.medium`: kept `vue` value over `laravel`.
- `priority.high`: kept `vue` value over `laravel`.
- `priority.critical`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `ticket.noteAdded`: kept `laravel` value over `adonis`.
- `ticket.unfollowed`: kept `laravel` value over `adonis`.
- `ticket.following`: kept `laravel` value over `adonis`.
- `ticket.created`: kept `vue` value over `adonis`.
- `rating.thankYou`: kept `vue` value over `adonis`.
- `inbound.disabled`: kept `rails` value over `adonis`.

### `fr`
- `status.reopened`: kept `vue` value over `laravel`.
- `priority.low`: kept `vue` value over `laravel`.
- `priority.medium`: kept `vue` value over `laravel`.
- `priority.high`: kept `vue` value over `laravel`.
- `priority.urgent`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `adonis`.
- `ticket.following`: kept `laravel` value over `adonis`.
- `ticket.created`: kept `vue` value over `adonis`.
- `ticket.reopened`: kept `laravel` value over `adonis`.
- `guest.created`: kept `laravel` value over `adonis`.
- `middleware.notAdmin`: kept `laravel` value over `adonis`.
- `inbound.disabled`: kept `rails` value over `adonis`.
- `priority.high`: kept `vue` value over `adonis`.

### `it`
- `status.inProgress`: kept `vue` value over `laravel`.
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `status.inProgress`: kept `vue` value over `nestjs`.
- `status.waitingOnCustomer`: kept `vue` value over `nestjs`.
- `status.waitingOnAgent`: kept `vue` value over `nestjs`.
- `activity.statusChanged`: kept `vue` value over `nestjs`.
- `activity.assigned`: kept `vue` value over `nestjs`.
- `activity.unassigned`: kept `vue` value over `nestjs`.
- `activity.priorityChanged`: kept `vue` value over `nestjs`.
- `activity.tagAdded`: kept `vue` value over `nestjs`.
- `activity.tagRemoved`: kept `vue` value over `nestjs`.
- `activity.replied`: kept `vue` value over `nestjs`.
- Additional conflicts omitted: 87.

### `ja`
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.following`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `ticket.reopened`: kept `laravel` value over `rails`.
- `ticket.customersCannotClose`: kept `laravel` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `bulk.updated`: kept `laravel` value over `rails`.
- `rating.alreadyRated`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `commands.install.success`: kept `laravel` value over `rails`.
- `status.reopened`: kept `vue` value over `nestjs`.
- `status.snoozed`: kept `laravel` value over `nestjs`.
- `activity.statusChanged`: kept `vue` value over `nestjs`.
- `activity.assigned`: kept `vue` value over `nestjs`.
- `activity.unassigned`: kept `vue` value over `nestjs`.
- Additional conflicts omitted: 83.

### `ko`
- `status.inProgress`: kept `vue` value over `laravel`.
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `status.closed`: kept `vue` value over `laravel`.
- `status.reopened`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `rating.onlyResolvedClosed`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `status.inProgress`: kept `vue` value over `nestjs`.
- `status.closed`: kept `vue` value over `nestjs`.
- `status.snoozed`: kept `laravel` value over `nestjs`.
- `status.unsnoozed`: kept `laravel` value over `nestjs`.
- `activity.statusChanged`: kept `vue` value over `nestjs`.
- `activity.assigned`: kept `vue` value over `nestjs`.
- Additional conflicts omitted: 92.

### `nl`
- `status.inProgress`: kept `vue` value over `laravel`.
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `status.escalated`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.following`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `rails`.
- `ticket.onlyInternalNotesPinned`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `rating.onlyResolvedClosed`: kept `laravel` value over `rails`.
- `rating.thanks`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `commands.install.success`: kept `laravel` value over `rails`.
- `status.inProgress`: kept `vue` value over `nestjs`.
- `status.waitingOnCustomer`: kept `vue` value over `nestjs`.
- `status.waitingOnAgent`: kept `vue` value over `nestjs`.
- Additional conflicts omitted: 87.

### `pl`
- `status.inProgress`: kept `vue` value over `laravel`.
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `status.resolved`: kept `vue` value over `laravel`.
- `status.closed`: kept `vue` value over `laravel`.
- `status.reopened`: kept `vue` value over `laravel`.
- `priority.medium`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.replySent`: kept `laravel` value over `rails`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.following`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `rails`.
- `ticket.onlyInternalNotesPinned`: kept `laravel` value over `rails`.
- `ticket.updated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `ticket.closed`: kept `laravel` value over `rails`.
- `ticket.reopened`: kept `laravel` value over `rails`.
- `ticket.customersCannotClose`: kept `laravel` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `guest.ticketClosed`: kept `laravel` value over `rails`.
- Additional conflicts omitted: 184.

### `pt-BR`
- `status.inProgress`: kept `vue` value over `laravel`.
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `status.escalated`: kept `vue` value over `laravel`.
- `priority.medium`: kept `vue` value over `laravel`.
- `priority.critical`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.following`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `rails`.
- `ticket.updated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `ticket.closed`: kept `laravel` value over `rails`.
- `ticket.reopened`: kept `laravel` value over `rails`.
- `ticket.customersCannotClose`: kept `laravel` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `guest.ticketClosed`: kept `laravel` value over `rails`.
- `bulk.updated`: kept `laravel` value over `rails`.
- `rating.onlyResolvedClosed`: kept `laravel` value over `rails`.
- `rating.alreadyRated`: kept `laravel` value over `rails`.
- Additional conflicts omitted: 132.

### `ru`
- `status.open`: kept `vue` value over `laravel`.
- `status.escalated`: kept `vue` value over `laravel`.
- `status.resolved`: kept `vue` value over `laravel`.
- `status.closed`: kept `vue` value over `laravel`.
- `status.reopened`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.macroApplied`: kept `laravel` value over `rails`.
- `ticket.following`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `rails`.
- `ticket.onlyInternalNotesPinned`: kept `laravel` value over `rails`.
- `ticket.updated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `ticket.closed`: kept `laravel` value over `rails`.
- `ticket.reopened`: kept `laravel` value over `rails`.
- `ticket.customersCannotClose`: kept `laravel` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `guest.ticketClosed`: kept `laravel` value over `rails`.
- `bulk.updated`: kept `laravel` value over `rails`.
- `rating.onlyResolvedClosed`: kept `laravel` value over `rails`.
- Additional conflicts omitted: 138.

### `tr`
- `status.open`: kept `vue` value over `laravel`.
- `status.inProgress`: kept `vue` value over `laravel`.
- `status.waitingOnCustomer`: kept `vue` value over `laravel`.
- `status.waitingOnAgent`: kept `vue` value over `laravel`.
- `status.escalated`: kept `vue` value over `laravel`.
- `status.resolved`: kept `vue` value over `laravel`.
- `status.closed`: kept `vue` value over `laravel`.
- `status.reopened`: kept `vue` value over `laravel`.
- `priority.low`: kept `vue` value over `laravel`.
- `priority.high`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.replySent`: kept `laravel` value over `rails`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.tagsUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.macroApplied`: kept `laravel` value over `rails`.
- `ticket.following`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `rails`.
- `ticket.onlyInternalNotesPinned`: kept `laravel` value over `rails`.
- `ticket.updated`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- Additional conflicts omitted: 190.

### `zh-CN`
- `status.open`: kept `vue` value over `laravel`.
- `status.reopened`: kept `vue` value over `laravel`.
- `ticket.created`: kept `vue` value over `laravel`.
- `ticket.noteAdded`: kept `laravel` value over `rails`.
- `ticket.assigned`: kept `laravel` value over `rails`.
- `ticket.unassigned`: kept `vue` value over `rails`.
- `ticket.statusUpdated`: kept `laravel` value over `rails`.
- `ticket.priorityUpdated`: kept `laravel` value over `rails`.
- `ticket.departmentUpdated`: kept `laravel` value over `rails`.
- `ticket.following`: kept `laravel` value over `rails`.
- `ticket.unfollowed`: kept `laravel` value over `rails`.
- `ticket.onlyInternalNotesPinned`: kept `laravel` value over `rails`.
- `ticket.created`: kept `vue` value over `rails`.
- `guest.created`: kept `laravel` value over `rails`.
- `bulk.updated`: kept `laravel` value over `rails`.
- `middleware.notAdmin`: kept `laravel` value over `rails`.
- `middleware.notAgent`: kept `laravel` value over `rails`.
- `commands.install.installing`: kept `laravel` value over `rails`.
- `commands.install.success`: kept `laravel` value over `rails`.
- `status.open`: kept `vue` value over `nestjs`.
- `activity.statusChanged`: kept `vue` value over `nestjs`.
- `activity.assigned`: kept `vue` value over `nestjs`.
- `activity.unassigned`: kept `vue` value over `nestjs`.
- `activity.priorityChanged`: kept `vue` value over `nestjs`.
- `activity.tagAdded`: kept `vue` value over `nestjs`.
- Additional conflicts omitted: 67.

## Locale Counts

- `ar`: 1843 keys
- `de`: 1843 keys
- `en`: 1843 keys
- `es`: 1843 keys
- `fr`: 1843 keys
- `it`: 1843 keys
- `ja`: 1843 keys
- `ko`: 1843 keys
- `nl`: 1843 keys
- `pl`: 1843 keys
- `pt-BR`: 1843 keys
- `ru`: 1843 keys
- `tr`: 1843 keys
- `zh-CN`: 1843 keys

## Consolidated Sources

### `adonis`
- `C:\Users\work\escalated-adonis\resources\lang\ar\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\de\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\en\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\es\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\fr\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\it\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\ja\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\ko\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\nl\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\pl\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\pt-BR\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\ru\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\tr\messages.json`
- `C:\Users\work\escalated-adonis\resources\lang\zh-CN\messages.json`

### `django`
- `C:\Users\work\escalated-django\escalated\locale\ar\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\de\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\en\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\es\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\fr\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\it\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\ja\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\ko\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\nl\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\pl\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\pt-BR\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\ru\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\tr\LC_MESSAGES\django.po`
- `C:\Users\work\escalated-django\escalated\locale\zh-CN\LC_MESSAGES\django.po`

### `dotnet`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.ar.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.it.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.ja.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.ko.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.nl.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.pl.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.pt-BR.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.ru.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.tr.resx`
- `C:\Users\work\escalated-dotnet\src\Escalated\Resources\Messages.zh-CN.resx`

### `filament`
- `C:\Users\work\escalated-filament\resources\lang\de\filament.php`
- `C:\Users\work\escalated-filament\resources\lang\en\filament.php`
- `C:\Users\work\escalated-filament\resources\lang\es\filament.php`
- `C:\Users\work\escalated-filament\resources\lang\fr\filament.php`

### `go`
- `C:\Users\work\escalated-go\locales\ar.json`
- `C:\Users\work\escalated-go\locales\it.json`
- `C:\Users\work\escalated-go\locales\ja.json`
- `C:\Users\work\escalated-go\locales\ko.json`
- `C:\Users\work\escalated-go\locales\nl.json`
- `C:\Users\work\escalated-go\locales\pl.json`
- `C:\Users\work\escalated-go\locales\pt-BR.json`
- `C:\Users\work\escalated-go\locales\ru.json`
- `C:\Users\work\escalated-go\locales\tr.json`
- `C:\Users\work\escalated-go\locales\zh-CN.json`

### `laravel`
- `C:\Users\work\escalated-laravel\resources\lang\ar\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\ar\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\ar\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\ar\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\ar\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\de\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\de\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\de\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\de\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\de\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\en\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\en\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\en\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\en\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\en\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\es\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\es\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\es\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\es\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\es\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\fr\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\fr\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\fr\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\fr\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\fr\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\it\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\it\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\it\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\it\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\it\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\ja\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\ja\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\ja\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\ja\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\ja\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\ko\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\ko\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\ko\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\ko\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\ko\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\nl\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\nl\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\nl\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\nl\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\nl\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\pl\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\pl\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\pl\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\pl\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\pl\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\pt_BR\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\pt_BR\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\pt_BR\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\pt_BR\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\pt_BR\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\ru\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\ru\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\ru\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\ru\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\ru\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\tr\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\tr\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\tr\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\tr\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\tr\notifications.php`
- `C:\Users\work\escalated-laravel\resources\lang\zh_CN\commands.php`
- `C:\Users\work\escalated-laravel\resources\lang\zh_CN\emails.php`
- `C:\Users\work\escalated-laravel\resources\lang\zh_CN\enums.php`
- `C:\Users\work\escalated-laravel\resources\lang\zh_CN\messages.php`
- `C:\Users\work\escalated-laravel\resources\lang\zh_CN\notifications.php`

### `nestjs`
- `C:\Users\work\escalated-nestjs\src\i18n\ar\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\it\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\ja\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\ko\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\nl\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\pl\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\pt-BR\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\ru\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\tr\messages.json`
- `C:\Users\work\escalated-nestjs\src\i18n\zh-CN\messages.json`

### `phoenix`
- `C:\Users\work\escalated-phoenix\priv\locales\ar.json`
- `C:\Users\work\escalated-phoenix\priv\locales\it.json`
- `C:\Users\work\escalated-phoenix\priv\locales\ja.json`
- `C:\Users\work\escalated-phoenix\priv\locales\ko.json`
- `C:\Users\work\escalated-phoenix\priv\locales\nl.json`
- `C:\Users\work\escalated-phoenix\priv\locales\pl.json`
- `C:\Users\work\escalated-phoenix\priv\locales\pt-BR.json`
- `C:\Users\work\escalated-phoenix\priv\locales\ru.json`
- `C:\Users\work\escalated-phoenix\priv\locales\tr.json`
- `C:\Users\work\escalated-phoenix\priv\locales\zh-CN.json`

### `rails`
- `C:\Users\work\escalated-rails\config\locales\ar.yml`
- `C:\Users\work\escalated-rails\config\locales\de.yml`
- `C:\Users\work\escalated-rails\config\locales\en.yml`
- `C:\Users\work\escalated-rails\config\locales\es.yml`
- `C:\Users\work\escalated-rails\config\locales\fr.yml`
- `C:\Users\work\escalated-rails\config\locales\it.yml`
- `C:\Users\work\escalated-rails\config\locales\ja.yml`
- `C:\Users\work\escalated-rails\config\locales\ko.yml`
- `C:\Users\work\escalated-rails\config\locales\nl.yml`
- `C:\Users\work\escalated-rails\config\locales\pl.yml`
- `C:\Users\work\escalated-rails\config\locales\pt-BR.yml`
- `C:\Users\work\escalated-rails\config\locales\ru.yml`
- `C:\Users\work\escalated-rails\config\locales\tr.yml`
- `C:\Users\work\escalated-rails\config\locales\zh-CN.yml`

### `spring`
- `C:\Users\work\escalated-spring\src\main\resources\messages_ar.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_it.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_ja.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_ko.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_nl.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_pl.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_pt_BR.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_ru.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_tr.properties`
- `C:\Users\work\escalated-spring\src\main\resources\messages_zh_CN.properties`

### `symfony`
- `C:\Users\work\escalated-symfony\translations\messages.ar.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.it.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.ja.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.ko.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.nl.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.pl.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.pt_BR.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.ru.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.tr.yaml`
- `C:\Users\work\escalated-symfony\translations\messages.zh_CN.yaml`

### `vue`
- `C:\Users\work\escalated\src\locales\ar.json`
- `C:\Users\work\escalated\src\locales\de.json`
- `C:\Users\work\escalated\src\locales\en.json`
- `C:\Users\work\escalated\src\locales\es.json`
- `C:\Users\work\escalated\src\locales\fr.json`
- `C:\Users\work\escalated\src\locales\it.json`
- `C:\Users\work\escalated\src\locales\ja.json`
- `C:\Users\work\escalated\src\locales\ko.json`
- `C:\Users\work\escalated\src\locales\nl.json`
- `C:\Users\work\escalated\src\locales\pl.json`
- `C:\Users\work\escalated\src\locales\pt-BR.json`
- `C:\Users\work\escalated\src\locales\ru.json`
- `C:\Users\work\escalated\src\locales\tr.json`
- `C:\Users\work\escalated\src\locales\zh-CN.json`

### `wordpress`
- `C:\Users\work\escalated-wordpress\languages\escalated-ar.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-de_DE.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-es_ES.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-fr_FR.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-it_IT.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-ja.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-ko_KR.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-nl_NL.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-pl_PL.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-pt_BR.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-ru_RU.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-tr_TR.po`
- `C:\Users\work\escalated-wordpress\languages\escalated-zh_CN.po`
- `C:\Users\work\escalated-wordpress\languages\escalated.pot`
