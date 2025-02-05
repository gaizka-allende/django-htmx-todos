from arrow import now, get

def formatTodoDate(created_modified):
  difference = now() - get(created_modified)

  if difference.days == 0: 
    return t('today')
  elif difference.days == 1:
    return 'Yesterday'
  elif difference.days == 2:
    return 'Two days ago'
  elif difference.days == 3:
    return 'Three days ago'
  elif difference.days == 4:
    return 'Four days ago'
  elif difference.days == 5:
    return 'five days ago'
  elif difference.days == 6:
    return 'Six days ago'
  elif difference.days >= 7 and difference.days < 14:
    return 'Last week'
  else:
    return 'More than two weeks ago'
