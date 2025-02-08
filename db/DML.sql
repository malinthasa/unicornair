
INSERT INTO plane (model, manufacturer, capacity, registration_number, status) VALUES
    ('A320', 'Airbus', 180, 'UA001', 'Active'),
    ('A321', 'Airbus', 220, 'UA002', 'Active'),
    ('B737-800', 'Boeing', 189, 'UA003', 'Active'),
    ('B747-400', 'Boeing', 416, 'UA004', 'Retired'),
    ('A350-900', 'Airbus', 325, 'UA005', 'Active'),
    ('B787-9', 'Boeing', 296, 'UA006', 'Active'),
    ('CRJ900', 'Bombardier', 90, 'UA007', 'Active'),
    ('E190', 'Embraer', 100, 'UA008', 'Active'),
    ('A330-300', 'Airbus', 277, 'UA009', 'Active'),
    ('B777-300ER', 'Boeing', 396, 'UA010', 'Active'),
    ('ATR 72', 'ATR', 72, 'UA011', 'Active'),
    ('A220-300', 'Airbus', 150, 'UA012', 'Active'),
    ('MD-88', 'McDonnell Douglas', 149, 'UA013', 'Retired'),
    ('A310', 'Airbus', 280, 'UA014', 'Retired'),
    ('B757-300', 'Boeing', 243, 'UA015', 'Under Maintenance'),
    ('B767-300', 'Boeing', 269, 'UA016', 'Active'),
    ('E195', 'Embraer', 124, 'UA017', 'Active'),
    ('A318', 'Airbus', 132, 'UA018', 'Active'),
    ('B737 MAX 8', 'Boeing', 178, 'UA019', 'Active'),
    ('Superjet 100', 'Sukhoi', 98, 'UA020', 'Active'),
    ('DC-9', 'McDonnell Douglas', 139, 'UA021', 'Retired'),
    ('BAe 146', 'British Aerospace', 112, 'UA022', 'Retired'),
    ('A340-300', 'Airbus', 295, 'UA023', 'Under Maintenance'),
    ('B707', 'Boeing', 202, 'UA024', 'Retired'),
    ('B737-400', 'Boeing', 168, 'UA025', 'Active'),
    ('A380-800', 'Airbus', 853, 'UA026', 'Active'),
    ('Tu-154', 'Tupolev', 180, 'UA027', 'Retired'),
    ('Fokker 100', 'Fokker', 97, 'UA028', 'Retired'),
    ('Dash 8 Q400', 'Bombardier', 78, 'UA029', 'Active'),
    ('Il-96', 'Ilyushin', 262, 'UA030', 'Under Maintenance');

INSERT INTO airport (airport_code, name, city, country, timezone) VALUES
    ('OSD', 'Åre Östersund Airport', 'Östersund', 'Sweden', 'Europe/Stockholm'),
    ('LYS', 'Lyon–Saint-Exupéry Airport', 'Lyon', 'France', 'Europe/Paris'),
    ('GVA', 'Geneva Airport', 'Geneva', 'Switzerland', 'Europe/Zurich'),
    ('NCE', 'Nice Côte dAzur Airport', 'Nice', 'France', 'Europe/Paris'),
    ('LED', 'Pulkovo Airport', 'Saint Petersburg', 'Russia', 'Europe/Moscow'),
    ('SOF', 'Sofia Airport', 'Sofia', 'Bulgaria', 'Europe/Sofia'),
    ('RIX', 'Riga International Airport', 'Riga', 'Latvia', 'Europe/Riga'),
    ('TLL', 'Tallinn Airport', 'Tallinn', 'Estonia', 'Europe/Tallinn'),
    ('VNO', 'Vilnius Airport', 'Vilnius', 'Lithuania', 'Europe/Vilnius'),
    ('KRK', 'John Paul II International Airport', 'Kraków', 'Poland', 'Europe/Warsaw'),
    ('PMI', 'Palma de Mallorca Airport', 'Palma', 'Spain', 'Europe/Madrid'),
    ('SVG', 'Stavanger Airport', 'Stavanger', 'Norway', 'Europe/Oslo'),
    ('GOT', 'Gothenburg Landvetter Airport', 'Gothenburg', 'Sweden', 'Europe/Stockholm'),
    ('TSF', 'Treviso Airport', 'Treviso', 'Italy', 'Europe/Rome'),
    ('MLA', 'Malta International Airport', 'Luqa', 'Malta', 'Europe/Malta'),
    ('OTP', 'Henri Coandă International Airport', 'Bucharest', 'Romania', 'Europe/Bucharest'),
    ('LUX', 'Luxembourg Airport', 'Luxembourg', 'Luxembourg', 'Europe/Luxembourg'),
    ('SKG', 'Thessaloniki Airport', 'Thessaloniki', 'Greece', 'Europe/Athens'),
    ('HER', 'Heraklion Airport', 'Heraklion', 'Greece', 'Europe/Athens'),
    ('FAO', 'Faro Airport', 'Faro', 'Portugal', 'Europe/Lisbon'),
    ('TXL', 'Berlin Tegel Airport', 'Berlin', 'Germany', 'Europe/Berlin'),
    ('MUC', 'Munich Airport', 'Munich', 'Germany', 'Europe/Berlin'),
    ('HAM', 'Hamburg Airport', 'Hamburg', 'Germany', 'Europe/Berlin'),
    ('CGN', 'Cologne Bonn Airport', 'Cologne', 'Germany', 'Europe/Berlin'),
    ('STR', 'Stuttgart Airport', 'Stuttgart', 'Germany', 'Europe/Berlin'),
    ('DUS', 'Düsseldorf Airport', 'Düsseldorf', 'Germany', 'Europe/Berlin'),
    ('NUE', 'Nuremberg Airport', 'Nuremberg', 'Germany', 'Europe/Berlin'),
    ('LEJ', 'Leipzig/Halle Airport', 'Leipzig', 'Germany', 'Europe/Berlin'),
    ('DRS', 'Dresden Airport', 'Dresden', 'Germany', 'Europe/Berlin'),
    ('HAJ', 'Hanover Airport', 'Hanover', 'Germany', 'Europe/Berlin'),
    ('FMO', 'Münster Osnabrück Airport', 'Münster', 'Germany', 'Europe/Berlin'),
    ('BRE', 'Bremen Airport', 'Bremen', 'Germany', 'Europe/Berlin'),
    ('SCN', 'Saarbrücken Airport', 'Saarbrücken', 'Germany', 'Europe/Berlin'),
    ('ERF', 'Erfurt-Weimar Airport', 'Erfurt', 'Germany', 'Europe/Berlin'),
    ('FDH', 'Friedrichshafen Airport', 'Friedrichshafen', 'Germany', 'Europe/Berlin'),
    ('PEK', 'Beijing Capital International Airport', 'Beijing', 'China', 'Asia/Shanghai'),
    ('PVG', 'Shanghai Pudong International Airport', 'Shanghai', 'China', 'Asia/Shanghai'),
    ('HND', 'Tokyo Haneda Airport', 'Tokyo', 'Japan', 'Asia/Tokyo'),
    ('NRT', 'Narita International Airport', 'Narita', 'Japan', 'Asia/Tokyo'),
    ('SIN', 'Singapore Changi Airport', 'Singapore', 'Singapore', 'Asia/Singapore'),
    ('BKK', 'Suvarnabhumi Airport', 'Bangkok', 'Thailand', 'Asia/Bangkok'),
    ('KUL', 'Kuala Lumpur International Airport', 'Kuala Lumpur', 'Malaysia', 'Asia/Kuala_Lumpur'),
    ('DEL', 'Indira Gandhi International Airport', 'Delhi', 'India', 'Asia/Kolkata'),
    ('BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'India', 'Asia/Kolkata'),
    ('MNL', 'Ninoy Aquino International Airport', 'Manila', 'Philippines', 'Asia/Manila'),
    ('HKG', 'Hong Kong International Airport', 'Hong Kong', 'Hong Kong', 'Asia/Hong_Kong'),
    ('TPE', 'Taiwan Taoyuan International Airport', 'Taipei', 'Taiwan', 'Asia/Taipei'),
    ('CGK', 'Soekarno-Hatta International Airport', 'Jakarta', 'Indonesia', 'Asia/Jakarta'),
    ('DPS', 'Ngurah Rai International Airport', 'Bali', 'Indonesia', 'Asia/Makassar'),
    ('SGN', 'Tan Son Nhat International Airport', 'Ho Chi Minh City', 'Vietnam', 'Asia/Ho_Chi_Minh'),
    ('HAN', 'Noi Bai International Airport', 'Hanoi', 'Vietnam', 'Asia/Ho_Chi_Minh'),
    ('DOH', 'Hamad International Airport', 'Doha', 'Qatar', 'Asia/Qatar'),
    ('RUH', 'King Khalid International Airport', 'Riyadh', 'Saudi Arabia', 'Asia/Riyadh'),
    ('JED', 'King Abdulaziz International Airport', 'Jeddah', 'Saudi Arabia', 'Asia/Riyadh'),
    ('FRA', 'Frankfurt Airport', 'Frankfurt', 'Germany', 'Europe/Berlin'),
    ('AMS', 'Amsterdam Schiphol', 'Amsterdam', 'Netherlands', 'Europe/Amsterdam'),
    ('MAD', 'Adolfo Suárez Madrid–Barajas', 'Madrid', 'Spain', 'Europe/Madrid'),
    ('BCN', 'Barcelona–El Prat Airport', 'Barcelona', 'Spain', 'Europe/Madrid'),
    ('VIE', 'Vienna International Airport', 'Vienna', 'Austria', 'Europe/Vienna'),
    ('CPH', 'Copenhagen Airport', 'Copenhagen', 'Denmark', 'Europe/Copenhagen'),
    ('ARN', 'Stockholm Arlanda Airport', 'Stockholm', 'Sweden', 'Europe/Stockholm'),
    ('OSL', 'Oslo Gardermoen Airport', 'Oslo', 'Norway', 'Europe/Oslo'),
    ('DUB', 'Dublin Airport', 'Dublin', 'Ireland', 'Europe/Dublin'),
    ('BRU', 'Brussels Airport', 'Brussels', 'Belgium', 'Europe/Brussels'),
    ('ZRH', 'Zurich Airport', 'Zurich', 'Switzerland', 'Europe/Zurich'),
    ('PRG', 'Václav Havel Airport Prague', 'Prague', 'Czech Republic', 'Europe/Prague'),
    ('WAW', 'Warsaw Chopin Airport', 'Warsaw', 'Poland', 'Europe/Warsaw'),
    ('BUD', 'Budapest Airport', 'Budapest', 'Hungary', 'Europe/Budapest'),
    ('ATH', 'Athens International Airport', 'Athens', 'Greece', 'Europe/Athens'),
    ('HEL', 'Helsinki Airport', 'Helsinki', 'Finland', 'Europe/Helsinki'),
    ('LIS', 'Lisbon Airport', 'Lisbon', 'Portugal', 'Europe/Lisbon'),
    ('JFK', 'John F. Kennedy International', 'New York', 'USA', 'America/New_York'),
    ('DXB', 'Dubai International Airport', 'Dubai', 'UAE', 'Asia/Dubai'),
    ('SYD', 'Sydney Kingsford Smith Airport', 'Sydney', 'Australia', 'Australia/Sydney'),
    ('CMB', 'Bandaranaike International Airport', 'Colombo', 'Sri Lanka', 'Asia/Colombo'),
    ('LAX', 'Los Angeles International Airport', 'Los Angeles', 'USA', 'America/Los_Angeles'),
    ('GRU', 'São Paulo–Guarulhos International Airport', 'São Paulo', 'Brazil', 'America/Sao_Paulo'),
    ('JNB', 'O. R. Tambo International Airport', 'Johannesburg', 'South Africa', 'Africa/Johannesburg'),
    ('MEX', 'Mexico City International Airport', 'Mexico City', 'Mexico', 'America/Mexico_City'),
    ('YYZ', 'Toronto Pearson International Airport', 'Toronto', 'Canada', 'America/Toronto'),
    ('EZE', 'Ministro Pistarini International Airport', 'Buenos Aires', 'Argentina', 'America/Argentina/Buenos_Aires'),
    ('SVO', 'Sheremetyevo International Airport', 'Moscow', 'Russia', 'Europe/Moscow'),
    ('ICN', 'Incheon International Airport', 'Seoul', 'South Korea', 'Asia/Seoul'),
    ('LHR', 'Heathrow Airport', 'London', 'United Kingdom', 'Europe/London'),
    ('CDG', 'Charles de Gaulle Airport', 'Paris', 'France', 'Europe/Paris');

INSERT INTO passenger (name, email) VALUES
('Malintha Adikari', 'malinthasa@gmail.com'),
('Bob Johnson', 'bob@example.com'),
('Charlie Brown', 'charlie@example.com');

INSERT INTO booking (passenger_id, flight_id) VALUES
(1, 'UAF001'),
(2, 'UAF002'),
(3, 'UAF003');
