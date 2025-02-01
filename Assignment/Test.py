import json
import hashlib
Hash={}
# Sample JSON string
json_data = '''{
  "head": null
}'''

# Parse JSON string
linked_list = json.loads(json_data)

# Function to traverse the linked list
def traverse_linked_list(node,hash):
    while node is not None:
        # print(node["data"])
        if(node["data"]==hash):
            print(Hash[hash]) 
            break
        node = node["next"]

# Function to add a new element to the linked list
def add_element(linked_list, new_data):
    data=hashlib.sha256(new_data.encode()).hexdigest()
    Hash[data]=new_data
    prev=None
    new_node = {"previous":prev ,"data": data, "next": None}
    if linked_list["head"] is None:  # If the list is empty
        linked_list["head"] = new_node
    else:
        current_node = linked_list["head"]
        while current_node["next"] is not None:
            current_node = current_node["next"]
        current_node["next"] = new_node
        new_node["previous"]=current_node

def modify(linked_list, new_data):
    data=hashlib.sha256(new_data.encode()).hexdigest()
    new_node = {"previous":None ,"data": data, "next": None}
    
    current_node = linked_list["head"]
    while(1):
        print(current_node["data"])
        if(current_node["data"]==data):
            print("Access Denied try a new node")
            return 1
        else:
            if(current_node["next"]==None):
                break
            current_node = current_node["next"]
        
    current_node["next"] = new_node
    new_node["previous"]=current_node
    Hash[data]=new_data

# Add a new element
add_element(linked_list, "MSG 1")
add_element(linked_list, "MSG 2")
add_element(linked_list, "MSG 3")
add_element(linked_list, "MSG 4")

hash_data=hashlib.sha256("MSG 4".encode()).hexdigest()
# Traverse and print the updated list
print("\nLinked list after adding a new element:")
traverse_linked_list(linked_list["head"],hash_data)

#Trying to modify an element
modify(linked_list, "MSG 4")
traverse_linked_list(linked_list["head"],hash_data)

# # Convert back to JSON if needed
# updated_json_data = json.dumps(linked_list, indent=2)
# print("\nUpdated JSON representation:\n", updated_json_data)

# print(linked_list)
