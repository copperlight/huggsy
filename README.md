[![release](https://github.com/copperlight/huggsy/actions/workflows/release.yml/badge.svg)](https://github.com/copperlight/huggsy/actions/workflows/release.yml)

# huggsy

Hi, I'm Huggsy, your penguin pal! If you summon me by name, I know how to do a few tricks:
 - `help | tell me more` - Display this message. I can be helpful.
 - `cat` - One cat image. Meow.
 - `dad joke | tell me a joke` - My best attempt at Dad joke humor.
 - `wow | owen` - What does the Owen say?

Example:

```
copperlight:black_cat:  9:22 PM
@Huggsy dad joke

HuggsyAPP  9:22 PM
Where did Captain Hook get his hook? From a second hand store.
```

See [configuration](./docs/configuration.md) docs for details on how this all fits together.

## Local Development

```shell
make setup-venv
make install-deps
make
```
