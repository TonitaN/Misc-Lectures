-- SAT application with the continuations used for backtracking.

--ghc 8.0.2
import Data.Map 
import qualified Data.Map as Map

sat :: BF
    -> Map String Bool
    -> (Bool -> Map String Bool -> r -> r)
    -> r
    -> r
sat bf asst gosucc gofail = case bf of
  Var v ->
    case Map.lookup v asst of
      Just b -> gosucc b asst gofail
      Nothing ->
        let asstT = Map.insert v True asst
            asstF = Map.insert v False asst
            tryF = gosucc False asstF tryT
            tryT = gosucc True asstT gofail
         in tryF

  Not bf' ->
    let succNot = gosucc . not
     in sat bf' asst succNot gofail

  And l r ->
    let succAnd True asstAnd failAnd = sat r asstAnd gosucc failAnd
        succAnd False asstAnd failAnd = gosucc False asstAnd failAnd
     in sat l asst succAnd gofail

  Or l r ->
    let succOr True asstOr failOr = gosucc True asstOr failOr
        succOr False asstOr failOr = sat r asstOr gosucc failOr
     in sat l asst succOr gofail

solve :: BF -> Maybe (Map String Bool)
solve bf =
  sat
    bf
    Map.empty
    (\b asst gofail -> if b then Just asst else gofail)
    Nothing

data BF = Var String | Not BF | And BF BF | Or BF BF

main = print $ solve $ (Not (Var "a") `Or` Var "b") `And` (Not (Var "b") `And` Var "c")