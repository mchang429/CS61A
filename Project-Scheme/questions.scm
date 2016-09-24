(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cddr x) (cdr (cdr x)))
(define (cadar x) (car (cdr (car x))))
(define (caddr x)   (car   (cdr (car (cdr x)))))

; Some utility functions that you may find useful to implement.
(define (map proc items)
  (if (null? items)
      nil
      (cons (proc (car items))
            (map proc (cdr items)))))

(define (cons-all first rests)
  (if (null? rests)
        ()
        (append (cons (cons first (car rests))  ()) (cons-all first (cdr rests))
  )
  )
)


(define (zip pairs)
    (if (null? pairs)
          (list nil nil)
            (append (cons (map car pairs) ()) (cons (map cadr pairs) ()))
    )
  )

;; Problem 18
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN Question 18
    (connect 0 s)
  )

(define (connect index list)
  (if (null? list)
      ()
      (cons (cons index (cons (car list) nil)) (connect (+ index 1) (cdr list)) )
)
)
  ; END Question 18


;; Problem 19
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN Question 19
  (cond
        ((null? denoms) ())
        ((> (car denoms) total) (list-change total (cdr denoms)))
        ((equal? (car denoms) total) (cons (cons(car denoms) ())(list-change total (cdr denoms))))
        (else
          (append (cons-all (car denoms) (list-change (- total (car denoms)) denoms))
                  (list-change total (cdr denoms)))
          )
        )
   )
)
  ; END Question 19

;; Problem 20
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (analyze expr)
  (cond ((atom? expr)
         ; BEGIN Question 20
         expr
         ; END Question 20
         )
        ((quoted? expr)
         ; BEGIN Question 20
         expr
         ; END Question 20
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN Question 20
          (cons 'lambda (cons params (analyze body)))
           ; END Question 20
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN Question 20
           (cons (cons 'lambda (list (map car values) (analyze (car body)))) (analyze (map cadr values)))
           ; END Question 20
           ))
        (else
         ; BEGIN Question 20
         (map analyze expr)
         ; END Question 20
         )))

;; Problem 21 (optional)
;; Draw the hax image using turtle graphics.
(define (hax d k)
  ; BEGIN Question 21
  'REPLACE-THIS-LINE
  )
  ; END Question 21

  (cons (cons  'lambda (cons(cons (caar values)
                      (cons (car (cadr values))  nil))
              body)

            )
         (cons (cadar values) (cons (caddr values) nil))
  )
