##  # later code
##  # jump down to see current step of the project
##
##  import asyncio
##  import dataclasses
##  import random
##  
##  
##  INDENT = "  "
##  
##  SCALE = 0.5
##  
##  T_BURGER = 7.5 / SCALE
##  T_FRIES  = 11  / SCALE
##  T_SODA   = 3   / SCALE
##  T_COOKIE = 7   / SCALE
##  
##  SEM_BURGER = asyncio.Semaphore(4)
##  SEM_FRIES  = asyncio.Semaphore(10)
##  SEM_SODA   = asyncio.Semaphore(6)
##  SEM_COOKIE = asyncio.Semaphore(3)
##  SEM_MANAGE = asyncio.Semaphore(4)
##  
##  
##  class Flavours:
##      burger = ["big_mac", "mac_n_cheese", "mac_bacon"]
##      fries = ["classic", "chedar", "roquefort", "onion"]   
##      soda = ["fanta", "coke", "sprite"]
##      cookie = ["chocolate", "vanella", "strawberry", "caramel"]
##  
##  
##  @dataclasses.dataclass
##  class Customer:
##      customer_id : int
##      flavour_burger : str
##      flavour_fries  : str
##      flavour_soda   : str
##      flavour_cookie : str
##  
##  
##  async def bake_burger(customer: Customer):
##      async with SEM_BURGER:
##          print("|", INDENT, f"--> Assembling a {customer.flavour_burger} for customer {customer.customer_id} ...")
##          await asyncio.sleep(T_BURGER)
##      print("|", INDENT, f"<-- Burger ready for customer {customer.customer_id}.")
##  
##  
##  async def bake_fries(customer: Customer):
##      async with SEM_FRIES:
##          print("|", INDENT , f"--> Frying {customer.flavour_fries} fries for customer {customer.customer_id} ...")
##          await asyncio.sleep(T_FRIES)
##      print("|", INDENT, f"<-- Fries are ready for customer {customer.customer_id}.")
##  
##  
##  async def bake_soda(customer: Customer):
##      async with SEM_SODA:
##          print("|", INDENT, f"--> Preparing a {customer.flavour_soda} for customer {customer.customer_id} ...")
##          await asyncio.sleep(T_SODA)
##      print("|", INDENT, f"<-- Soda ready for customer {customer.customer_id}.")
##  
##  
##  async def bake_cookie(customer: Customer):
##      async with SEM_COOKIE:
##          print("|", INDENT, f"--> Baking {customer.flavour_cookie} cookie for customer {customer.customer_id} ...")
##          await asyncio.sleep(T_COOKIE)
##      print("|", INDENT, f"<-- Cookie ready for customer {customer.customer_id}.")
##  
##  
##  async def manage(customer: Customer):
##      async with SEM_MANAGE:
##          await asyncio.sleep(random.randint(1, 4))
##          print(f"| --> Considerating customer {customer.customer_id}'s order ...")
##          await asyncio.gather(
##              bake_burger(customer),
##              bake_fries(customer),
##              bake_soda(customer),
##              bake_cookie(customer)
##          )
##      print(f"|  <-- Customer {customer.customer_id}'s order is ready !")
##  
##  
##  async def main_func(n_customers: int):
##      print("| ---------- Welcome to McDo ! ---------\n| ")
##      queue = []
##      for i in range(0, n_customers):
##          customer = Customer(i, 
##              random.sample(Flavours.burger, 1)[0], 
##              random.sample(Flavours.fries, 1)[0], 
##              random.sample(Flavours.soda, 1)[0], 
##              random.sample(Flavours.cookie, 1)[0]
##          )
##          manager = manage(customer)
##          queue.append(manager)
##      await asyncio.gather(*queue)
##      print("|\n| --------------- END ------------------")
##      
##  
##  loop = asyncio.new_event_loop()
##  asyncio.set_event_loop(loop)
##  loop.run_until_complete(main_func(4))
##  
## 
 
# current starter code

import asyncio

async def task1() -> None:
    await asyncio.sleep(0.7)
    print("cat!")
    
async def task2() -> None:
    await asyncio.sleep(0.5)
    print("pussy", end=" ")

async def task3() -> None:
    await asyncio.sleep(1)
    print("a", end=" ")
    await asyncio.gather(task1(), task2())

async def task4() -> None:
    await asyncio.sleep(0.5)
    print("am", end=" ")

async def main() -> None:
    print("Hello!")
    await asyncio.sleep(1.75)
    print("I", end=" ")    
    await asyncio.gather(task3(), task4())


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())

# same code, but in a one single lambda function :-)

main = lambda: (lambda time: (lambda loop, task, sleep, nest, gather: (
    # logic part, to use with this nice AST :
    #   task → synchronous call
    #   sleep → non-blocking delay
    #   nest → sequence of tasks and delays
    #   gather → similar to asyncio.gather, accepts only nests
    # use loop() to run the code

    ## ...BEGIN PROGRAM SECTION...

    loop(
        nest(
            task(print, "Hello!"),
            sleep(1.75),
            task(print, "I", end=" "),
            gather(
                nest(
                    sleep(1),
                    task(print, "a", end=" "),
                    gather(
                        nest(
                            sleep(0.7),
                            task(print, "cat!"),
                        ),
                        nest(
                            sleep(0.5),
                            task(print, "pussy", end=" "),
                        )
                    ),
                ),
                nest(
                    sleep(0.5),
                    task(print, "am", end=" "),
                )  
            )
        )
    )

    ## ...END PROGRAM SECTION...
 
))(
    # Scheduler loop that walks the task tree
    lambda tree_nest: (lambda walker, loop_iter_table=[True]: (tree_nest.__setitem__(2, time.time()), [(walker(walker, tree_nest, [True], [False], []), loop_iter_table.append(True) if tree_nest[1] else None) for i in loop_iter_table]))( 
        # The tree walker, decides wether to execute a task, wait on a sleep, recurse into a nest, interleave gather branches
        lambda walker, nest, walker_iter_table, break_flag, delete_later: ([((
                    # The executor, makes each line live
                    lambda line, clear, break_: ((
                        line[1](*line[2], **line[3]), clear()) if line[0] == "task" else (
                        break_() if time.time() < (nest[2] + line[1]) else (clear(), nest.__setitem__(2, time.time()))) if line[0] == "sleep" else (
                        walker(walker, line, [True], [False], []), break_() if line[1] else clear()) if line[0] == "nest" else (
                        [(inner_nest.__setitem__(2, time.time()) if inner_nest[2] is None else None, walker(walker, inner_nest, [True], [False], []) if inner_nest[1] else line[1].remove(inner_nest)) for inner_nest in line[1]], break_() if line[1] else (clear(), nest.__setitem__(2, time.time()))) if line[0] == "gather" else None))(
                    # Arguments for the executor 
                    nest[1][index], 
                    lambda: delete_later.append(True), 
                    lambda: break_flag.__setitem__(0, True)),
                    # Reiterates the walker loop, checks wether there are pending tasks or not in the tree
                    (walker_iter_table.append(True)) if not break_flag[0] and index < (len(nest[1]) - 1) else None,
                    # Unpolls the cpu
                    time.sleep(0.01))
                # Walker loop, reiterates only if not break_flag
                for index, _ in enumerate(walker_iter_table)], 
            # Deletes executed lines
            [(nest[1].__delitem__(0)) for i in delete_later])),
    # Data types
    lambda func, *args, **kwargs: ["task", func, args, kwargs], # type task   [tname; func; args of func; keyword args of func]
    lambda t_sec:  ["sleep", t_sec],                            # type sleep  [tname; time in seconds to wait]
    lambda *tasks: ["nest", list(tasks), None],                 # type nest   [tname; list of tasks; local time when the nest is processed for the first time]
    lambda *nests: ["gather", list(nests)]                      # type gather [tname; list of nests]
))(__import__("time"))

skeleton = main()