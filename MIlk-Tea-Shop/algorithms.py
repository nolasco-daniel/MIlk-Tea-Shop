def bubble_sort(arr, key=None, reverse=False):
    n = len(arr)
    result = arr.copy()
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if key:
                left_val = key(result[j])
                right_val = key(result[j + 1])
            else:
                left_val = result[j]
                right_val = result[j + 1]
            
            should_swap = left_val > right_val if not reverse else left_val < right_val
            
            if should_swap:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        
        if not swapped:
            break
    
    return result

def levenshtein_distance(s1, s2):
  if len(s1) < len(s2):
      return levenshtein_distance(s2, s1)
  
  if len(s2) == 0:
      return len(s1)
  
  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
      current_row = [i + 1]
      for j, c2 in enumerate(s2):
          insertions = previous_row[j + 1] + 1
          deletions = current_row[j] + 1
          substitutions = previous_row[j] + (c1 != c2)
          current_row.append(min(insertions, deletions, substitutions))
      previous_row = current_row
  
  return previous_row[-1]

def normalized_levenshtein(s1, s2):
    if not s1 and not s2:
        return 0.0
    
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    
    if max_len == 0:
        return 0.0
        
    return distance / max_len

def fuzzy_search_score(query, text, threshold=0.3):
    if not query or not text:
        return 0
        
    query = query.lower()
    text = text.lower()
    
    if query in text:
        return 100
    
    words = text.split()
    best_score = 0
    
    for word in words:
        norm_distance = normalized_levenshtein(query, word)
        
        if norm_distance <= threshold:
            similarity = 1 - norm_distance
            word_score = int(similarity * 100)
            best_score = max(best_score, word_score)
    
    return best_score

