# Notes — data-types-and-data-structures

# Data types and Data structures

**Operators**

| power | `**` |
| --- | --- |
| division | `/` |
| integer division | `//` |
| modulo | `%` |

```
# .find('x'): returns the lowest index where a given substring is found (-1 if not found)
'hello world'.find('l')
```

```
# .index('x'): same idea but returns Error if not found
'hello world'.index('l')
```

```
# .format() : replace the {} in the string by what you want. Useful to write strings with variable arguments.
'{} loves{}'.format('Mary', 'python')
```

```
# An even more optimized method : f-strings
f"{a} loves{b}."
```

**Dictionaries**

```jsx
dictionary.get('key1') : get the value1 for the key1 of this dictionnary
```

```jsx
dictionary[key1] : get the value1 for the key1 of this dictionnary
```

**Set**

```jsx
# Using a set to remove duplicates from a list
lst = ['Tokyo', 'Berlin', 'Helsinki', 'Rio', "Denver", "Tokyo", "Berlin"]
lst
```

```jsx
['Tokyo', 'Berlin', 'Helsinki', 'Rio', 'Denver', 'Tokyo', 'Berlin']
```

```jsx
set(lst)
```

**List**

```jsx
# .append(): adds elements to the end of the list
numbers.append(8)
# Be careful : if you use it with another list, it will insert a list in a list
numbers.append([9, 10, 11])
```

```jsx
# .extend(): incorporates elements from another list to the list
numbers.extend([15, 16, 17])
```