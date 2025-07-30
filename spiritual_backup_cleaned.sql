-- authorized_admins
DROP TABLE IF EXISTS authorized_admins;

CREATE TABLE authorized_admins (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(20) DEFAULT NULL,
  CONSTRAINT unique_phone UNIQUE (phone)
);

INSERT INTO authorized_admins (id, name, phone) VALUES
(1, 'Nitin', '9552271965')
ON CONFLICT (id) DO NOTHING;

-- bhaktgan
DROP TABLE IF EXISTS bhaktgan;

CREATE TABLE bhaktgan (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) DEFAULT NULL,
  phone VARCHAR(20) DEFAULT NULL,
  seva_interest TEXT,
  location VARCHAR(255),
  submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT unique_name_email UNIQUE (name, email),
  CONSTRAINT bhaktgan_unique_entry UNIQUE (name, email, phone)
);

INSERT INTO bhaktgan (id, name, email, phone, seva_interest, location, submitted_at) VALUES
(12,'Pratiksha Jadhav','pratikshasuryawanshi1994@gmail.com','9588437122','Rangoli kadhne','Pune','2025-07-21 16:30:04'),
(18,'Nitin Jadhav','jadhavnitin75@gmail.com','9552271965','Ashram seva','Pune','2025-07-25 13:44:34')
ON CONFLICT (id) DO NOTHING;

-- contact_details
DROP TABLE IF EXISTS contact_details;

CREATE TABLE contact_details (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20) DEFAULT NULL,
  message TEXT NOT NULL,
  submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT unique_contact_entry UNIQUE (name, phone, email)
);

INSERT INTO contact_details (id, name, email, phone, message, submitted_at) VALUES
(1, 'Nitin', 'jadhavnitin75@gmail.com', NULL, 'धन्यवाद', '2025-07-21 07:07:15'),
(4, 'Nitin', 'jadhavnitin75@gmail.com', '9552271965', 'Hi', '2025-07-21 09:03:52')
ON CONFLICT (id) DO NOTHING;

-- daily_programs
DROP TABLE IF EXISTS daily_programs;

CREATE TABLE daily_programs (
  id SERIAL PRIMARY KEY,
  date DATE DEFAULT NULL,
  content TEXT,
  created_by VARCHAR(255) DEFAULT NULL
);

INSERT INTO daily_programs (id, date, content, created_by) VALUES
(7, '2025-07-27', 'आज बाबा बद्रिनाथ धामचे दर्शन करुन परत लातुरला आले त्यानिमित्त आज रात्री ०७ वाजता बोपला येथे स्नेह भोजनाचा कार्यक्रम आयोजीत केला आहे.', 'Nitin'),
(8, '2025-07-28', 'आज श्रावण महिण्यातला पहीला सोमवार आसल्यामुळे बाबा महादेवाची भक्ती करीत आहेत.', 'Nitin')
ON CONFLICT (id) DO NOTHING;

-- sadguru_thoughts
DROP TABLE IF EXISTS sadguru_thoughts;

CREATE TABLE sadguru_thoughts (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  added_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sadguru_thoughts (id, content, added_on) VALUES
(1, 'सेवा म्हणजेच अध्यात्माचे मूळ आहे.', '2025-07-22 15:50:14'),
(2, 'बे वजह किसी पर अधिकार जमाने का प्रयत्न ना करो||\nआपका उतना समर्पण होगा तो अधिकार भी अपने आप सिध्द होगा.', '2025-07-23 05:52:48'),
(3, 'सब को एक दोरे मे बांधते-बांधते शरीर पुरी तरह थक चुका है|\nअब डर लगता है कही डोरी तुटते ही सब बीखर न जाये.', '2025-07-23 06:11:26'),
(4, 'हे महादेव! सब चीज हाशील है दुनिया की मुझे\nबस अब तुमसे एकरुप होने की तमन्ना है मुझे', '2025-07-23 06:11:26'),
(5, 'प्रत्येक व्यक्ती अपने अपने कार्यक्षेत्र मे अपने\nकर्तव्य को पुरी निष्ठा से बरकरार रखे||', '2025-07-23 06:11:26'),
(6, 'सब को एक दोरे मे बांधते-बांधते शरीर पुरी तरह थक चुका है|\nअब डर लगता है कही डोरी तुटते ही सब बीखर न जाये.', '2025-07-24 14:31:35'),
(7, 'हे महादेव! सब चीज हाशील है दुनिया की मुझे\nबस अब तुमसे एकरुप होने की तमन्ना है मुझे', '2025-07-24 14:31:35'),
(8, 'प्रत्येक व्यक्ती अपने अपने कार्यक्षेत्र मे अपने\nकर्तव्य को पुरी निष्ठा से बरकरार रखे||', '2025-07-24 14:31:35')
ON CONFLICT (id) DO NOTHING;

-- wisdom_quotes
DROP TABLE IF EXISTS wisdom_quotes;

CREATE TABLE wisdom_quotes (
  id SERIAL PRIMARY KEY,
  quote TEXT NOT NULL,
  author VARCHAR(100) DEFAULT NULL
);

INSERT INTO wisdom_quotes (id, quote, author) VALUES
(1, 'Yoga is the journey of the self, through the self, to the self.', 'Bhagavad Gita'),
(2, 'Responsibility is the highest form of action.', 'Sadhguru'),
(3, 'Silence isn’t empty — it’s full of answers.', 'Anonymous')
ON CONFLICT (id) DO NOTHING;
