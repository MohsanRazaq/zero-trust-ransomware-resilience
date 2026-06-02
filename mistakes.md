### Threading

##PROBLEM
i was   stuck for too long time on "THREADING lock "  and "RACING CONDITION"
  ## SOLUTION:
  i introduced  a lock_ method so only one method can use process  and after completing  control moves to next process


  ###problem
  first i onlylocking out toplevel folders leaving inner sub folders un access able and program quietly exit,

  ##solution

  so i ultemately learn the technique  when locking--> go deepest and then  locking out   
  and when unlocking start with with top folder   