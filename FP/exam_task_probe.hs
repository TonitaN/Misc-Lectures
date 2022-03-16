--ghc 8.0.2

main = print $ elimTaut (Or (Or (Var 'A') (Or (Var 'C') (Not (Var 'A')))) (Not (Or (Var 'B') ValT))) id

data Log a = Var a | ValT | Not (Log a) | Or (Log a) (Log a) deriving (Eq, Show)

elimTaut :: Log Char -> (Log Char -> Log Char) -> Log Char

elimTaut (Or v1 (Not v2)) cont = elimTaut v1 (cont.(check (elimTaut v2 id)))
               where check x1 x2 | x1 == x2 = ValT
                                 | otherwise = x2 `Or` (Not x1) 
elimTaut (Or v1 v2) cont = elimTaut v1 (cont.(\v -> v `Or` (elimTaut v2 id)))
elimTaut (Not v) cont = elimTaut v (cont.(\v1 -> Not $ v1))
elimTaut w cont = cont w