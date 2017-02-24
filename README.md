# Analytic-Research-Programming
Programming Assignment for Analytics Research &amp; Implementation

For this model, we decided to take two different approaches in booking the airplane, and test both of these against numerous cases. The first model looked at placing passengers continuously (if there's enough to sit together) from front to back in a snake like form, straight across the aisle. The second model looks at row-by-row by each booking. For example, Booking 1 has 3 passengers, Booking 2 has 2 passengers, and Booking 3 has 3 passengers. Instead of filling them across (like Model 1), this model will put Booking 1 in Row 1, Booking 2 in Row 2, Booking 3 in Row 3 and so on. Once the model reaches the last row, it will go back and fill in the rest of the seats with priority keeping everyone together. Also, for the passengers seperated metric, we assumed that if they are not in the same row, then they will be considered seperated.

With numerous tests, we found that Model 2 was successful in all test runs, and will be using that as our final submission.
