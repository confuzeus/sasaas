# SaaS Cookiecutter Boilerplate

This boilerplate can be used to quickly start a SaaS project.

## Features

- Single configuration source (.env).
- Complete authentication system.
    - Authenticate with Email and Password.
    - Or social accounts.
- Antispam with [hcaptcha](https://hcaptcha.com).
- User profile management.
- Bootstrap 5 and jQuery for quick frontend development.
- Asset pipeline with [Gulp](https://gulpjs.com/).
- Backgroung tasks with [django-q](https://django-q.readthedocs.io/en/latest/).

## How to use Memberships

Memberships use `Group` from `django.contrib.auth`.

1. Configure `MEMBERSHIP_GROUPS` in settings.py.
    - It's a `dict` that takes a `str` unique code  as key and group name as value.
2. Configure `VIEW_PERMISSION_GROUPS`.
    - It's a `dict` that takes a unique `str` view id as key and a `list` of allowed groups.
3. Configure `UPGRADE_URL`.
    - This is where users who don't have access to a view will be redirected to.
    - Preferably, this should be the page where users are asked to upgrade their membership.
4. Decorate your views with `group_required` from the `core` package.
    - This decorator takes a unique `str` view_id.
    - This is the view id that must be used in `VIEW_PERMISSION_GROUPS` from above.
5. Configure a `DEFAULT_MEMBERSHIP_GROUP`.
    - This is the group that new users will be added to by default.
6. Run the `init_membership` management command.
    - This command adds all current users who aren't part of any membership groups to the default one you specified above.

Some example settings have been set already and you can find some dummy views in the `accounts` app.

## Roadmap

- [x] Add membership functionality.
- [ ] Add Stripe.