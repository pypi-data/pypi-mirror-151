# Cairo type hints
Add type hints to your Cairo-lang files and feed the generated json files to Stark-Dot-Net code generators.

## Install
```bash
pip install cairo-type-hints
```

## Example usage:
```bash
python cairo-type-hints/console.py \
    -i ./src/my-awesome-contract.cairo \
    -o ./artifacts/hints/test-hints.json
```

## Adding hints to structs
A type hint is a comment with a colon, a space and then a type. Valid types are `int`, `string`, and `address`. For example, `#: int`.

Type hints are added inline per member of the struct. For example:

```cairo-lang
struct UserMeta:
    member index : felt #: int
    member hash : felt
    member position : Position
end
```

Members without a type hint will default to `string` for `felt` and the struct type for structs.

The above Cairo-lang example outputs:
```json
[
   {
      "name":"UserMeta",
      "members":[
         {
            "type":"int",
            "name":"index"
         },
         {
            "type":"string",
            "name":"hash"
         },
         {
            "type":"Position",
            "name":"position"
         }
      ],
      "type":"struct"
   }
]
```

## Adding hints to functions
Function hint comments mimic Cairo-lang function type declarations and are placed as the first statement in a function body. For example:

```
#: (index : int, position : Position) -> (user : User)
```

```cairo-lang
@view
func get_user_by_index {
    syscall_ptr : felt*, pedersen_ptr : HashBuiltin*,
    range_check_ptr
    } (index : felt, position : Position) -> (user : User):
    #: (index : int, position : Position) -> (user : User)
    let (hash) = users_index_to_hash.read(index)
    let (user) = get_user_by_hash(hash)
    return (user = user)
end
```

The above Cairo-lang example outputs:

```json
[
    {
      "name":"get_user_by_index",
      "inputs":[
         {
            "type":"int",
            "name":"index"
         },
         {
            "type":"Position",
            "name":"position"
         }
      ],
      "outputs":[
         {
            "type":"User",
            "name":"user"
         }
      ],
      "type":"function"
   }
]
```

## Development

Install and switch to python 3.9.x
```bash
$ pyenv install 3.9.9
$ pyenv local 3.9.9
```

Create a virtual environment and activate it
```bash
$ python -m venv env
$ source venv/bin/activate
```

Do some awesome work!

## Build and publish the package
```bash
$ python setup.py bdist_wheel sdist
$ twine upload dist/*
```