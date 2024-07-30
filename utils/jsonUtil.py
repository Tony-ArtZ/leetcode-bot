import json

def store(userId, leetcodeId):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    data[userId] = leetcodeId
    
    with open('data.json', 'w') as f:
        json.dump(data, f)

def get(userId):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        result = data.get(userId)
        return result
    except FileNotFoundError:
        print("File not found")
        return None
    except KeyError:
        print(f"User ID {userId} not found")
        return None