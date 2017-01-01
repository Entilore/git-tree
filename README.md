gitTree
====

List contents of repository in a tree-like format, using .gitignore to hide files

## Demo

![git-tree.png](https://qiita-image-store.s3.amazonaws.com/0/21173/51cd4acc-e1bc-fe64-203b-6aef08ac8c60.png "git-tree.png")

## Requirement
 - python

## Usage
```
$git-tree
```
or
```
$git tree
```

The result can be exported to a latex file with this way:
```
$git-tree -o file.tex
```

Some other file might be ignored with a regex like pattern: 
```
$git-tree -i "someFile|someOtherFile"
```

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[kosystem](https://github.com/kosystem)
[entilore](https://github.com/entilore)
