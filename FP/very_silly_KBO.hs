--ghc 8.0.2

main = print $ 
    checKBO [(Dos "a" (Cero "Z") (Var "y"), Uno "s" $ Var "y"),
 (Dos "a" (Uno "s" $ Var "x") (Cero "Z"), Dos "a" (Var "x") (Uno "s" $ Cero "Z")),
 (Dos "a" (Uno "s" $ Var "x") (Uno "s" $ Var "y"), Dos "a" (Dos "a" (Uno "s" $ Var "x") (Var "y")) (Var "x"))
 ]
    [] printOrd []

data Term a b = Var b | Cero a | Uno a (Term a b) | Dos a (Term a b) (Term a b) deriving (Eq, Show)

instance Foldable (Term a) where
  foldr f seed (Var n) = f n seed
  foldr f seed (Cero f1) = seed
  foldr f seed (Uno f1 arg) = foldr f seed arg
  foldr f seed (Dos f1 arg1 arg2) = foldr f (foldr f seed arg1) arg2

instance Functor (Term a) where
  fmap f (Var x) = Var $ f x
  fmap f (Cero x) = Cero x
  fmap f (Uno f1 arg) = Uno f1 (fmap f arg)
  fmap f (Dos f1 arg1 arg2) = Dos f1 (fmap f arg1) (fmap f arg2)

type TRS a b = [(Term a b, Term a b)]

ismem term lst = foldr (||) False (map (term == ) lst)

closure term lst
  | (ismem term lst) == True = lst
  | otherwise = clos2 [] term lst
  where clos2 lst term [] = (term : lst)
        clos2 lst term@(f1,f2) (term'@(f3,f4):lst')
           | f1 == f4 = closure (f3,f2) (clos2 (term':lst) term lst')
           | f2 == f3 = closure (f1,f4) (clos2 (term':lst) term lst')
           | otherwise = clos2 (term':lst) term lst'

listing (Dos f1 arg1 arg2) = (f1, [arg1, arg2])
listing (Uno f1 arg1) = (f1, [arg1])
listing (Cero name) = (name, [])
listing (Var name) = ([], [])

listfail [] trs ord success failure = failure
listfail (rule:rest) trs ord success failure = listfail rest trs ord success (checKBO (rule:trs) ord success failure)

lexic (x1 : xs1) (x2 : xs2) | x1 == x2 = lexic xs1 xs2
                            | otherwise = [(x1,x2)]
lexic x1 x2 = []

checKBO [] ord success failure = success ord
checKBO ((Var n1, Var n2):rest) ord success failure = failure
checKBO ((Var n1, Cero n2):rest) ord success failure = checKBO rest ord success failure
checKBO ((t1, Var n):rest) ord success failure
   | foldr (||) False (fmap (== n) t1) == True = checKBO rest ord success failure
   | otherwise = failure
checKBO ((t1, t2) :rest) ord success failure
     | foldr (||) False (fmap (== t2) (snd $ listing t1)) = checKBO rest ord success failure
     | (ismem (f1,f2) ord) == True = checKBO ((fmap ((,) t1)  args2) ++ rest) ord success failure
     | (ismem (f2,f1) ord) == True = listfail (fmap (flip (,) t2)  args1) rest ord success failure
     | f1 == f2 && (length args1 == length args2) = checKBO ((fmap ((,) t1)  args2) ++ (lexic args1 args2) ++ rest) ord success failure
     | f1 /= [] = checKBO ((fmap ((,) t1)  args2) ++ rest) (closure (f1,f2) ord) success 
                                                (listfail (fmap (flip (,) t2)  args1) rest ord success failure)
     | otherwise = failure
     where
       (f1, args1) = listing t1
       (f2, args2) = listing t2

printOrd lst = show lst
