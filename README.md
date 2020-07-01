# redis_check
Tests redis cluster which node that is master (writeable) and swaps master-slave roles. 
Ex:
```bash
$ python redis_swap.py
No action requested, add -s (--swap) or -c (--check) as argument
```

```
$ python redis_swap.py -c
-- Current state
redisk01 {'state': 'running', 'role': 'slave'}
redisk02 {'state': 'running', 'role': 'master'}
```

```
python redis_swap.py -s
-- Current state
redisk01 {'state': 'running', 'role': 'slave'}
redisk02 {'state': 'running', 'role': 'master'}
-- New state
redisk01 {'state': 'running', 'role': 'master'}
redisk02 {'state': 'running', 'role': 'slave'}
[root@redisk01 ~]#
```
