# Day 1 - 2026-10-02

## 1. list

### What it is
`list` 用来保存一组有顺序的数据。

### Example
```python
customers = ["Toyota", "Honda", "Nissan"]
```

### Key points
- 用 `[]` 创建。
- 可以保存多个值。
- 可以通过索引访问。
- 可以配合 `for` 循环逐个处理。

### In today's project
`customer_cases` 是一个 list，里面保存了多个 customer case。

---

## 2. dict

### What it is
`dict` 用 `key: value` 的方式保存结构化数据。

### Example
```python
customer = {
    "customer": "Toyota",
    "issue": "Cannot login",
    "priority": "high"
}
```

### Key points
- 用 `{}` 创建。
- 通过 key 读取数据。
- 很适合表示一条业务记录。
- API 返回的 JSON 数据经常和 dict 很接近。

### Access value
```python
customer["priority"]
```

---

## 3. for loop

### What it is
`for` 用来重复处理一组数据。

### Example
```python
for customer in customer_cases:
    print(customer["customer"])
```

### Key points
- 每次循环处理一条数据。
- `customer` 是当前循环里使用的临时变量。
- 常用于处理 list、dict、API 返回结果。

---

## 4. if / elif / else

### What it is
用来根据不同条件执行不同逻辑。

### Example
```python
if priority == "high":
    ...
elif priority == "medium":
    ...
else:
    ...
```

### Key points
- `if`：第一个条件。
- `elif`：其他条件。
- `else`：前面条件都不成立时执行。
- 适合处理确定性的业务规则。

### Business example
不同 priority 对应不同 SLA：
- high → 1 hour
- medium → 4 hours
- low → 24 hours

---

## 5. function

### What it is
function 用来把一段可以重复使用的逻辑封装起来。

### Example
```python
def get_sla(priority):
    if priority == "high":
        return "1 hour"
```

### Key points
- `def` 用来定义函数。
- 参数写在 `()` 中。
- 定义函数 ≠ 执行函数。
- 必须调用函数，函数体才会真正运行。

### Call
```python
get_sla("high")
```

---

## 6. return

### What it is
`return` 用来把函数计算后的结果返回出去。

### Example
```python
def get_sla(priority):
    return "1 hour"
```

### Key points
- `return` 会把结果交回调用函数的位置。
- `return` 之后，当前函数通常就结束了。
- 返回值可以保存到变量，也可以直接用于 `print()`。

### Example
```python
sla = get_sla("high")
print(sla)
```

也可以直接：

```python
print(get_sla("high"))
```

---

## 7. f-string

### What it is
f-string 用来把变量或表达式放进字符串。

### Example
```python
name = "Toyota"
print(f"Customer: {name}")
```

### Key points
- 字符串前面加 `f`。
- 变量或表达式写在 `{}` 中。
- 通常比使用 `+` 拼接字符串更容易阅读。

### Comparison
不太推荐：

```python
print("Customer: " + name)
```

更推荐：

```python
print(f"Customer: {name}")
```

---

## 8. dict.items()

### What it is
`.items()` 可以同时读取 dictionary 的 key 和 value。

### Example
```python
for key, value in priority_count.items():
    print(f"{key}: {value}")
```

### Key points
直接遍历 dictionary：

```python
for key in priority_count:
```

通常只能得到 key。

使用：

```python
priority_count.items()
```

可以同时得到 key 和 value。

---

## 9. `in` keyword

### What it is
`in` 可以判断一个值是否存在于某个数据结构中。

### Example
```python
if priority in priority_count:
    priority_count[priority] += 1
```

### Today's use
判断当前 priority 是否是 `priority_count` 里的一个 key。

例如：

```python
"high" in priority_count
```

如果 `priority_count` 里有 `"high"` 这个 key，就会返回 `True`。

---

## 10. `+= 1`

### What it is
`+= 1` 表示在原来的数字基础上增加 1。

### Example
```python
priority_count["high"] += 1
```

等价于：

```python
priority_count["high"] = priority_count["high"] + 1
```

### Today's use
用来统计不同 priority 各出现了多少次。

---

## 11. Temporary variables

### Example
```python
priority = customer["priority"]
```

这不是必须的，也可以直接写：

```python
customer["priority"]
```

### Why use a temporary variable?
- 减少重复代码。
- 提高可读性。
- 后续调试更方便。
- 当表达式比较长时尤其有用。

### Rule of thumb
- 只使用一次：可以直接使用原表达式。
- 会重复使用多次：通常值得先保存到一个变量。

---

## 12. Basic Debugging

### Bug encountered
曾经错误调用：

```python
priority_plus(priority_count)
```

但是 `priority_plus()` 期待的参数应该是：

```python
"high"
"medium"
"low"
```

而实际传入的是整个 dictionary。

因此：

```python
if priority == "high":
```

不成立；

```python
elif priority == "medium":
```

也不成立；

```python
elif priority == "low":
```

也不成立。

最终进入：

```python
else:
    priority_count["unknown"] += 1
```

于是 `unknown` 被额外增加了一次。

### Lesson
Debug 时优先检查：

1. function 期待什么参数。
2. 实际传入了什么值。
3. 传入的数据类型是什么。
4. 程序实际进入了哪个条件分支。
5. 是否有函数被多调用了一次。

---

# Project Built

## Customer Issue SLA Parser

### Current functions
- 保存多个 customer case。
- 输出 customer / issue / priority。
- 根据 priority 判断 SLA。
- 处理 unknown priority。
- 统计各 priority 的数量。

### Example structure
```python
customer_cases = [
    {
        "customer": "Toyota",
        "issue": "Cannot login to the system",
        "priority": "high"
    }
]
```

### SLA function
```python
def get_sla(priority):
    sla_level = "SLA: Response within "

    if priority == "high":
        return f"{sla_level}1 hour"
    elif priority == "medium":
        return f"{sla_level}4 hours"
    elif priority == "low":
        return f"{sla_level}24 hours"
    else:
        return "Unknown priority"
```

### Priority statistics
```python
priority_count = {
    "high": 0,
    "medium": 0,
    "low": 0,
    "unknown": 0
}

for customer in customer_cases:
    priority = customer["priority"]

    if priority in priority_count:
        priority_count[priority] += 1
    else:
        priority_count["unknown"] += 1

print("Priority Summary")

for key, value in priority_count.items():
    print(f"{key}: {value}")
```

---

# Key Engineering Takeaways

1. 一条结构化业务数据可以用 `dict` 表示。
2. 多条业务数据可以使用 `list[dict]` 表示。
3. 确定性的业务规则适合直接使用 Python 实现，而不是全部交给 LLM。
4. function 可以把业务逻辑封装起来，提高可读性和复用性。
5. 异常输入应该明确处理，而不是默认当作某种正常情况。
6. 结构化数据本身可以帮助减少大量重复的 `if / elif`。
7. Debug 时，要关注输入值、参数、数据类型和实际执行路径。
8. “代码能运行”只是第一步；还要考虑可读性、异常情况和后续维护。

---

# Agent / Enterprise AI Connection

今天虽然还没有真正开始写 AI Agent，但已经接触了以后会反复出现的基础概念：

- `dict` → 结构化业务数据、JSON、API response。
- `list[dict]` → 多条工单、客户记录、任务列表。
- function → Tool / business logic 的基础。
- if / else → deterministic business rules。
- unknown handling → input validation / error handling。
- priority statistics → 后续 evaluation / monitoring 的基础思路。

一个重要原则：

> 能够由确定性代码稳定完成的事情，不需要全部交给 LLM 判断。

未来的 Enterprise Agent 往往会是：

```text
LLM / Agent
    ↓
理解模糊需求、做语义判断
    ↓
Python / API / Business Rules
    ↓
确定性地执行企业业务逻辑
```

---

# Tomorrow

计划继续学习：

- string methods
- list methods
- dict methods
- file read / write
- 让 customer data 从文件读取，而不是全部 hard-code 在 Python 文件里
