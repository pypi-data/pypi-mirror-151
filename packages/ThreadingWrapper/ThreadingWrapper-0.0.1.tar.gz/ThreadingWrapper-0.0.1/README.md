# pythreading-wrapper


> pip install pythreading-wrapper


usage

```commandline

from concurrency import FunctionArgs, MultiThreading

# a long running process that returns results based on 
# a parameter passed

def long_running_process(param1: int):
    time.sleep(1)
    return param1
    
# imagine a large data set that needs to be chunked
 
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
def chunk(start: int, end: int):
    return data[start:end]

if __name__ == "__main__":
    
    mp = MultiThreading()
    
    # run the process 5 times in parallel
    # the resturn types will be captured inside a dictionary
    
    #--------------------------------------------------------
    # use case 1 : getting data for different parameters passed 
    args = [FunctionArgs(long_running_process, output_var=item, param1=item) for item in range(5)]
    op: dict = threading.execute_async(*args)
    assert len(op.items()) == 5  # will be True
    assert op[1] == 1  # will be 1
    assert op[2] == 2  # will be 2
    assert op[3] == 3  # will be 3
    assert op[4] == 4  # will be 4
    
    #--------------------------------------------------------
    # use case 2 : getting data by chunks from a large dataset
    # run the process 5 times in parallel
    # the resturn types will be captured inside a dictionary
    
    args = [FunctionArgs(chunk, output_var='', start=item, end=item+2) for item in range(0, 10, 2)]
    op: list = threading.execute_by_chunks_async(*args)
    print(op)
    assert data[1] in op # op will contain 1
    assert data[3] in op # op will contain 3
    assert data[5] in op # op will contain 5
    assert data[7] in op # op will contain 7

```