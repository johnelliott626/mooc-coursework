-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = 'Chamberlin Street';

--Found: Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. 
--Interviews were conducted today with three witnesses who were present at the time — 
--each of their interview transcripts mentions the courthouse.

SELECT transcript
FROM interviews
WHERE transcript LIKE '%courthouse%';

--I work at the courthouse, and I saw the hit-and-run on my way into work this morning.
--I saw him talking on the phone outside the courthouse at 3:00pm.
--Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
--I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
--As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT license_plate, activity 
FROM courthouse_security_logs
WHERE hour = 10 AND minute > 15 AND minute <= 25;

--license_plate | activity
--N7M42GP | entrance
--Y340743 | entrance
--5P2BI95 | exit
--94KL13X | exit
--6P58WS2 | exit
--4328GD8 | exit
--G412CB7 | exit
--L93JTIZ | exit
--322W7JE | exit
--0NTHK55 | exit
--P14PE2Q | entrance
--1M92998 | entrance
--PF37ZVK | exit
--1M92998 | exit
--XE95071 | exit
--IH61GO8 | exit
--8P9NEU9 | exit

SELECT account_number, transaction_type, year
FROM atm_transactions
WHERE atm_location = 'Fifer Street' 
AND transaction_type = 'withdraw'
AND month = 7 AND day = 28;

--account_number | transaction_type | year
--28500762 | withdraw | 2020
--28296815 | withdraw | 2020
--76054385 | withdraw | 2020
--49610011 | withdraw | 2020
--16153065 | withdraw | 2020
--25506511 | withdraw | 2020
--81061156 | withdraw | 2020
--26013199 | withdraw | 2020

SELECT id, name, phone_number, passport_number FROM (people JOIN bank_accounts ON people.id = bank_accounts.person_id) 
WHERE (license_plate IN
(SELECT license_plate
FROM courthouse_security_logs
WHERE hour = 10 AND minute > 15 AND minute <= 25 AND activity = 'exit'))
AND 
(account_number IN
(SELECT account_number
FROM atm_transactions
WHERE atm_location = 'Fifer Street' 
AND transaction_type = 'withdraw'
AND month = 7 AND day = 28));

--    id | name   | phone_number   | passport_number
--686048 | Ernest | (367) 555-5533 | 5773159633
--514354 | Russell | (770) 555-1861 | 3592750733
--396669 | Elizabeth | (829) 555-5269 | 7049073643
--467400 | Danielle | (389) 555-5198 | 8496433585

SELECT caller, receiver, duration
FROM phone_calls
WHERE caller IN
(SELECT phone_number FROM (people JOIN bank_accounts ON people.id = bank_accounts.person_id) 
WHERE (license_plate IN
(SELECT license_plate
FROM courthouse_security_logs
WHERE hour = 10 AND minute > 15 AND minute <= 25 AND activity = 'exit'))
AND 
(account_number IN
(SELECT account_number
FROM atm_transactions
WHERE atm_location = 'Fifer Street' 
AND transaction_type = 'withdraw'
AND month = 7 AND day = 28)))
AND day = 28 AND month = 7
AND duration < 60;

--caller | receiver | duration
--(367) 555-5533 | (375) 555-8161 | 45 ---> caller: Ernest receiver: Berthold
--(770) 555-1861 | (725) 555-3243 | 49 ---> caller: Russel receiver: Philip

SELECT name FROM people 
WHERE phone_number = '(375) 555-8161' OR phone_number = '(725) 555-3243';

SELECT destination_airport_id, passport_number
FROM flights JOIN passengers ON flights.id = passengers.flight_id
WHERE passport_number IN
(SELECT passport_number 
FROM people 
WHERE phone_number = '(367) 555-5533' OR phone_number = '(770) 555-1861')
AND month = 7 AND day = 29 AND hour = 8;

--destination_airport_id | passport_number
--4 | 5773159633

SELECT name 
FROM people
WHERE passport_number = 5773159633;
--Ernest

SELECT city 
FROM airports 
WHERE id = 4;
--London