--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Ubuntu 14.17-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.17 (Ubuntu 14.17-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: countries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.countries (
    id integer NOT NULL,
    value character varying,
    name character varying
);


ALTER TABLE public.countries OWNER TO postgres;

--
-- Name: countries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.countries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.countries_id_seq OWNER TO postgres;

--
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.countries_id_seq OWNED BY public.countries.id;


--
-- Name: document_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_types (
    id integer NOT NULL,
    value character varying,
    name character varying
);


ALTER TABLE public.document_types OWNER TO postgres;

--
-- Name: document_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_types_id_seq OWNER TO postgres;

--
-- Name: document_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_types_id_seq OWNED BY public.document_types.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    title character varying,
    country_id integer,
    document_type_id integer,
    year_id integer,
    image character varying,
    pdf character varying
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.documents_id_seq OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: years; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.years (
    id integer NOT NULL,
    value integer,
    name integer
);


ALTER TABLE public.years OWNER TO postgres;

--
-- Name: years_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.years_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.years_id_seq OWNER TO postgres;

--
-- Name: years_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.years_id_seq OWNED BY public.years.id;


--
-- Name: countries id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries ALTER COLUMN id SET DEFAULT nextval('public.countries_id_seq'::regclass);


--
-- Name: document_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_types ALTER COLUMN id SET DEFAULT nextval('public.document_types_id_seq'::regclass);


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: years id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.years ALTER COLUMN id SET DEFAULT nextval('public.years_id_seq'::regclass);


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.countries (id, value, name) FROM stdin;
1	ASM	American Samoa
2	COK	Cook Islands
3	FJI	Fiji
4	PYF	French Polynesia
5	FSM	Federated States of Micronesia
6	GUM	Guam
7	KIR	Kiribati
8	MHL	Marshall Islands
9	NRU	Nauru
10	NIU	Niue
11	MNP	Northern Mariana Islands
12	NCL	New Caledonia
13	PLW	Palau
14	PNG	Papua New Guinea
15	SLB	Solomon Islands
16	WSM	Samoa
17	TKL	Tokelau
18	TON	Tonga
19	TUV	Tuvalu
20	VUT	Vanuatu
21	WLF	Wallis and Futuna
\.


--
-- Data for Name: document_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document_types (id, value, name) FROM stdin;
1	tidecalendar	Tide Calendar
2	waveclimate	Wave Climate Report
3	geodetic	Geodetic Survey Report
\.


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents (id, title, country_id, document_type_id, year_id, image, pdf) FROM stdin;
1	Tonga - Neiafu	18	1	1	a042b1f924774e72965dbd8312f07de2_img.png	a10ec99cb69f4ef68b10802460c06c59_pdf.pdf
2	Tuvalu - Nukulaelae	19	1	1	9458fc84fce44b96980b6f5275063186_img.png	2e809ead4e374bcdb3062da60c556f8b_pdf.pdf
3	Tuvalu - Niutao	19	1	1	5f42b423ed904c51801fe7d187d63a72_img.png	6f867f2f3d54491781d09958238ab914_pdf.pdf
4	Vanuatu - Port Villa	20	1	1	6485b5a7a72e4bdbab644c6ccef92cc0_img.png	566fda7b7f324e76b986ca7504d50d31_pdf.pdf
5	Tonga - Nuku'alofa	18	1	1	aef7ac5ea44449cd9401d5f50200e775_img.png	142dfca98c8c4bc3abb61cdd2a180ba3_pdf.pdf
6	FSM - Pohnpei	5	1	1	0c1a2a95b3d04006835f1fd88227a656_img.png	60ae637d28e34ccca13cc44b00c93c32_pdf.pdf
7	Nauru - Nauru	9	1	1	5fe242b46d794d448c99c4402cac3b54_img.png	a3cd38457ba94f5cac8bf5f60880f34f_pdf.pdf
8	Tuvalu - Funafuti	19	1	1	80b38e00a2ae47ebaaa2ab5ba2579428_img.png	b83ee79352c640dbb34e22116c8be5ab_pdf.pdf
9	Vanuatu - Lenakel	20	1	1	b14bb8659dca43bfaa59a4c8c8c1251c_img.png	580761132a624daaa6ec8e9d32668630_pdf.pdf
10	COK - Penrhyn	2	1	1	d05d6fe9a68c494093d603c9c5e9a7e8_img.png	535932cd65534009928a3490f0ed775a_pdf.pdf
11	COK - Rarotonga	2	1	1	9bc8c4d3997741caa0011adbfe652553_img.png	80dd0578d7ee45c5a52e5f30af2db42d_pdf.pdf
12	Tuvalu - Nanumaga	19	1	1	6778f9beefda456aad82c656d942fc3e_img.png	e7b404b8f5704b01be75feb05b5ce295_pdf.pdf
13	Fiji - Vatia	3	1	1	8250303970d748d4928a885cfc98ba7a_img.png	b1f1bf9d23d34d7d9aa088ae1878f379_pdf.pdf
14	MHL - Ebeye	8	1	1	b5de8d9ac3fa4b2387241aa5ff1c14ae_img.png	930043fc744f431f8a3d4b1c673d74ac_pdf.pdf
15	Kiribati - Betio	7	1	1	7a291be34603432ba441a4338b71a314_img.png	ca14ce679ba54c29a05845037e0bb47b_pdf.pdf
16	SLB - Honiara	15	1	1	8d31e1d94d1e4e7f9ff4b3c4f9972eb9_img.png	22f16da937b24925ae63e1a74a80f1f5_pdf.pdf
17	Vanuatu - Malekula	20	1	1	fd16438f0e5d4ac59b783509ec07cd3e_img.png	d0e0441365e444c0b87c3f47299e0a49_pdf.pdf
18	Vanuatu - Luganville	20	1	1	5b1ad01aa9fa493c8a1f6f8af8e4a6bb_img.png	78828ee0c4214e49be55a6d270b49119_pdf.pdf
19	Tuvalu - Nui	19	1	1	3afaaca6bb914b3ea1eec9c483aafab8_img.png	c139caeb6eff4c6086ff9bb288781a46_pdf.pdf
20	American Samoa - Pago Pago	1	1	1	a3fe4b82c2e04c758015f3dc35575331_img.png	8192e84fad9143deb7a63a5795d33915_pdf.pdf
21	Kiribati - Kiritimati	7	1	1	e3b077a11bd14b65b450a9406ded0c9e_img.png	264cfa69a0a84c3cb600c82aeca8ddc9_pdf.pdf
22	Tuvalu - Vaitupu	19	1	1	d2a9441a48644fb392b53106c54fdc8e_img.png	81927b28f9e94aa7b83eeb913a408421_pdf.pdf
23	Palau - Malakal	13	1	1	1f71de45cdd44d88975b7d35ca0f817a_img.png	303a2903205a4790914c07342b8de00f_pdf.pdf
24	Tuvalu - Nukufetau	19	1	1	ecf4ef8f16eb4372a3072fdbeee21188_img.png	19e1be062a49402a82ff7c160cf2942a_pdf.pdf
25	MHL - Majuro	8	1	1	2547aa1ab67c4600b983372474fb7150_img.png	cb4a69eb0ce346f2b1b69d95311a76a2_pdf.pdf
26	SLB - Tarekukure	15	1	1	44574211994d4a1f800b9b738ed4a03f_img.png	ab81d0f1d21e426281edd445d73f8189_pdf.pdf
27	Fiji - Port Denarau	3	1	1	6a990307f0f9431c8c7f3f8136b25c06_img.png	5a0961973f97485cba13a2236349a27d_pdf.pdf
28	Tuvalu - Niulakita	19	1	1	88e92644427043c6a87d31a6faa72963_img.png	6348101fedd04eb8957189f05e06eb93_pdf.pdf
29	PNG - Port Moresby	14	1	1	fd7e1cfa3ed34ddebe6b58defe738616_img.png	96d4801ee3b24ac6910ab15e85fba566_pdf.pdf
30	Samoa - Apia	16	1	1	aedae57d6c1d4be089d5ed7cae92c0b0_img.png	2a2361db42c64e9d90f98cfa50cc525f_pdf.pdf
31	Kiribati - Kanton	7	1	1	cb17e585c5a24a0c840dbb41fb6dbe52_img.png	c506824be40346de9c9031a137faa6cf_pdf.pdf
32	Fiji - Lautoka	3	1	1	53f340e7be9c4dd382ed9c7666ba7b44_img.png	674f1d628c5d431b8626fdcbc0446e3c_pdf.pdf
33	PNG - Lombrum	14	1	1	eb2228e21ed54bfabb845b23f5939674_img.png	0a8c16b17e724161bd0812e1c7bdf2fb_pdf.pdf
34	Tuvalu - Nanumea	19	1	1	ab601571a77a494f8b79e4cc41a927fd_img.png	8776b9886b58477dbe6fb0af6cede68e_pdf.pdf
35	SLB - Lata Wharf	15	1	1	0afe57f65f5e475380756eef2682ae45_img.png	c95624d49c70446bb47877515df44517_pdf.pdf
36	Niue - Niue	10	1	1	a751f45d82cf49c98bf3fd5e123840df_img.png	80c1b424703b48e5a25a7cc6f2525499_pdf.pdf
37	Fiji - Suva	3	1	1	a34137524d9d4306a70d6e5cad99a6ad_img.png	4c68c9d0809f4a87bdf81d94ce8f110f_pdf.pdf
38	Tokelau - Atafu	17	1	1	0aa0169f02a740f48ea21eec022fc498_img.png	3d450277237449bcb57654359a8d1bea_pdf.pdf
39	Tokelau - Nukunonu	17	1	1	0399dee3614c40fcafa4b52e88550f06_img.png	fc108b4d6be44ec18c90615bfb3c38cc_pdf.pdf
40	Tokelau - Fakaofo	17	1	1	a27bf4a81a0043efb465c96905c54cfa_img.png	3c34e9dfa68c4f498ff37617ed754801_pdf.pdf
41	SLB - Lata Whart	15	1	2	53a89f67e96e416f9c6260776621305b_img.png	bf80775668fc4259a350410271adb6aa_pdf.pdf
42	PNG - Lombrum	14	1	2	7f8360eec58344aaa6f6ee96bad3dd00_img.png	d62fd8f227f643208edef0ae30082302_pdf.pdf
43	Fiji - Lautoka	3	1	2	14379e4420a54e7081088e937e50a5fc_img.png	6ac61b7f52ca43fc8d36e189bbf42fa0_pdf.pdf
44	Kiritibati - Kanton	7	1	2	b830591163d24695b9c25f8e133840f1_img.png	7ad6ba762c0945d1b5ea223ce80b97db_pdf.pdf
45	Kiritibati - Betio	7	1	2	28a2b482675540b993dec806a017b2f2_img.png	99c14c465e7f4c6f97de4360f6fc27d1_pdf.pdf
46	PNG - Port Moresby	14	1	2	021ae68c7fc7475bb3ad0ce1e3f2d001_img.png	8db2779c781745e9bd289967a26b864f_pdf.pdf
47	MHL - Majuro	8	1	2	b03adb91b0cf4bb4a996ff0a9d8fca59_img.png	987253d067c84faebe1e73560eb4fd24_pdf.pdf
48	Palau - Malakal	13	1	2	1296465e2c27488fa7ed4119d92b2200_img.png	3db4b6a211b24a569269801324cc6ff4_pdf.pdf
49	Tonga - Neiafu	18	1	2	29ea10cd0091442ca1f88359c5f90632_img.png	fea346bd87b549629b8b3eff08714c7e_pdf.pdf
50	Samoa - Apia	16	1	2	9a15e75894cf48ed9845e017c03ee0be_img.png	4d622d4a7ee241ecb5c8cd924f18a57d_pdf.pdf
51	Vanutu - Luganville	20	1	2	7cd8720c7e9b4bbda198cb88565242d0_img.png	7f6ac00f890c43ec9512251f3390f0c2_pdf.pdf
52	Fiji - Suva	3	1	2	d6b993067df644688c811b6dd58f337d_img.png	fcb5c91ca1d1486a9f98665fb3919c49_pdf.pdf
53	COK - Rarotonga	2	1	2	e99bd991e62e46ba85082082b0a9994a_img.png	5dd47e1f8d794f6f970f0f6417640079_pdf.pdf
54	Vanuatu - Port Villa	20	1	2	692e19f8c6ac467c81e3922c6de6dec6_img.png	d284b76ebf644b38a83f52053a8f2d1e_pdf.pdf
55	Tonga - Nuku'alofa	18	1	2	15cf1b470f204dbb9f55dbc63cc39ecf_img.png	9fff00da023c4e8ebf0dfa42574c61e3_pdf.pdf
56	Tuvalu - Funafuti	19	1	2	8678d21247c440b2bd9169a8687a07ac_img.png	4706e1de95db469dbaf17f878a2df499_pdf.pdf
57	Nauru	9	1	2	e0a92210a52d4ff0bbbe08b209f6bbee_img.png	a8326f72db7643e9a3d21f33a1047faf_pdf.pdf
58	Tuvalu - Vaitupu	19	1	2	f6d6aa8ea7724a6597ed80c721078177_img.png	34be86f725a24d33af9e870a22322e71_pdf.pdf
59	COK - Penrhyn	2	1	2	393afdc6780744e487d0886ba0f07fdc_img.png	fa30cab07c4443d5855180fbf8113dee_pdf.pdf
60	FSM - Pohnpei	5	1	2	6d5df12efaf24112baff36e9da262a6d_img.png	8beaf257c1ae42a384b66849c9d5f82e_pdf.pdf
61	Niue	10	1	2	16258ce103d5439d964318cb08bd7e90_img.png	b48d7818ab7f4ff0ade3f0a02c698d09_pdf.pdf
62	Kiritibati - Kiritimati	7	1	2	7681859c740b495ebdb4afbbfb42bc61_img.png	b32d16133d0f48ababac3644cd14cd59_pdf.pdf
63	SLB - Tarekukure	15	1	2	12578a980b1c4b278a4d308054228ea0_img.png	5a09b3caf00845f5a2a358850444e2be_pdf.pdf
64	MHL - Ebeye	8	1	2	6e47f829ff09437a981ceac84c8f2dcc_img.png	a1596d8ad3f842689c88a127724ce4a2_pdf.pdf
65	SLB - Honiara	15	1	2	8832d079c9a54678880da3205b7c5a25_img.png	1cf231c6ed424971b0955f8971fef56c_pdf.pdf
66	Kiribati - Betio	7	2	3	9a040e8f8f8c4005ada97e63d1961951_img.png	56ad2306969847a18da5453f2b586f4e_pdf.pdf
67	Kiribati - Fanning	7	2	3	9b199a5484724fd68d8a678973b6bac3_img.png	ac2695c9530f4e1c945d427fba5ea1e9_pdf.pdf
68	Kiribati - Bonriki	7	2	3	abb554b10c6245e38a0d873a03bb94e8_img.png	73467adf8d1e49acaf6306db10d8fdc5_pdf.pdf
69	Kiribati - Canton	7	2	3	0ef908a823b846849091f6bfd304e763_img.png	e1ff73c2a54940c8878acd7c5418a4b0_pdf.pdf
70	Kiribati - Kiritimati	7	2	3	085b5cfaa772441c8087534307f9673b_img.png	4f1c3a6ae4884e44815af1784dd7e766_pdf.pdf
71	Tonga - Nuku'alofa	18	2	3	6a83036941624b068a6619df506429f4_img.png	cec80323a4e243f7a8b5c3eb51040d39_pdf.pdf
72	Tonga - Neiafu	18	2	3	aefb5d64d7d4410ba292c8e1bdb6503e_img.png	646912898d734a1e8c0a37ae3d4b62de_pdf.pdf
73	Tonga - Lifuka	18	2	3	f92a2991003c4662848f0fbc1e1ed5bc_img.png	9cbe349ea41348888f0c94eb762232c5_pdf.pdf
74	Tonga - 'Eua	18	2	3	e3ae1af3c6274cd6a44b15abf74dced0_img.png	47f505ecb75a405e977190d37d779898_pdf.pdf
75	Tonga - Tonga	18	2	3	5cc874dc5b184358ba003585973c07fa_img.png	965cc8c58f6e4934a0e613c90a6b3d29_pdf.pdf
76	Tonga - Pangai	18	2	3	16fe685b320f4f95bd6b0390c749020f_img.png	4d827e1ff02f47639baf38634473d2cb_pdf.pdf
77	Tonga - TongaWB1	18	2	3	715e02bc6a1c477fb9e7f98f896a087a_img.png	330c8453ec8e434e8b8553a5610634ec_pdf.pdf
78	Tonga - Niuas	18	2	3	d6e2fcbac41e446da65e928e8513edf5_img.png	0ed46fd89d204a06bdec9bf8ddc7f581_pdf.pdf
79	Wallis - Leava	21	2	3	79b8359288874b989ea123073d9bab72_img.png	56251b89f71d40c7b8baae0fd0d6698c_pdf.pdf
80	Wallis - Honikulu	21	2	3	88e0e6c1eb7b46a3b872dc191b6c7aea_img.png	0e4bd0b9e36e4d94b43dd2ca3b36361d_pdf.pdf
81	French Polynesia - Rikitea	4	2	3	68a5ed58e1bd40f1b2b4d5b54b7b921a_img.png	35d40fe346424d438396e2a32d9fb9d3_pdf.pdf
82	French Polynesia - Nuku	4	2	3	bc44bc9895f74493878f636ba6b4e930_img.png	cafd73f61275497ba1a609ce6f6da6af_pdf.pdf
83	French Polynesia - Rurutu	4	2	3	8778d62c026643868906e90b33dbda17_img.png	11588735a2894e13aed1246c7d5dafe0_pdf.pdf
84	French Polynesia - Bora	4	2	3	4b1aa4f65c324ee9aa40fc2aa2d14cbb_img.png	844f66059ade4c2b92ef362cb5b8f515_pdf.pdf
85	French Polynesia - Raivavae	4	2	3	ebdfdcc0808040a896d3cbc52c41b214_img.png	d6f46f566b9f46c58bb08f71ce4b4070_pdf.pdf
86	French Polynesia - Hiva	4	2	3	d0a63793296440e8a718fea80492e050_img.png	aad70ac553c74b6d8b19295f6025eecc_pdf.pdf
87	French Polynesia - Rangiroa	4	2	3	032cdde8e7d64915b91ef47b9de1e905_img.png	a9d5db7212c9499d9f74db8a339020b8_pdf.pdf
88	French Polynesia - Papeete	4	2	3	7d1a1defe9a7474295bbcc93db56712c_img.png	6a422d6b324a4530aa62c0fe527a4ecf_pdf.pdf
89	French Polynesia - Fakarava	4	2	3	e2f82bbbe1cb4edf85d40769547a1eb8_img.png	34ae5b502bc84d0ca8209236971fb7bf_pdf.pdf
90	French Polynesia - Tubuai	4	2	3	92e7ac0f6b9841c9b9220bdb292bbd80_img.png	956e5297b2db41afa1150b95c52ac646_pdf.pdf
91	French Polynesia - Rimatara	4	2	3	579928a0605b4b71a9dd3dba6e774dc5_img.png	3945e52d34e64b52949b01e590cde8b6_pdf.pdf
92	American Samoa - Pago	1	2	3	7bafc3bfb012462099c3847e8b60cc45_img.png	b08e24130392497c9d4ca237103aea6d_pdf.pdf
93	American Samoa - Tau	1	2	3	e5f173c4db6b4b40bc5607ed8a659a39_img.png	fd2217fe5ec241028d6f0fd7dbf07007_pdf.pdf
94	Fiji - Kadavu	3	2	3	e96f79ea47be450d9a05285c672de376_img.png	869b08f3e87b49909d965ed002bc1714_pdf.pdf
95	Fiji - Ono-i-Lau	3	2	3	f8f99c2c41d04556ac316e0b44376cdd_img.png	e79c8a661fc54dd99a597ef5f57de6cc_pdf.pdf
96	Fiji - Savusavu	3	2	3	537c8d2c931e4e69a2db9effe21908bb_img.png	ff2aff55267c47d48094b24b183b3381_pdf.pdf
97	Fiji - Vanua	3	2	3	15c6025dc86f425dae0bf2d236e6eb28_img.png	fdf2675a0db24de48917d412a1de415b_pdf.pdf
98	Fiji - Taveuni	3	2	3	7901edeed602443ba9ced152d59c8b84_img.png	1a2efe8233a3493cadb49bec3488d700_pdf.pdf
99	Fiji - Suva	3	2	3	4f09c74ac86a4b16b8d534bd800169ab_img.png	2f26bddd5ccb4c46bedcc965772b937d_pdf.pdf
100	Fiji - Beqa	3	2	3	5900c387d5374739ada298c1e95d034a_img.png	e5319aba3e1a42eba09fb3c3ee38c0ae_pdf.pdf
101	Fiji - Labasa	3	2	3	6080ec96374b4e57bc630b85acf5c2a3_img.png	df8295318c8a4ddd97953998a4929b12_pdf.pdf
102	Fiji - Lakepa	3	2	3	5432125660634ad8abccf68848523907_img.png	393949526b6445aa94c3effe9acb087a_pdf.pdf
103	Fiji - Gau	3	2	3	46dc0e3fc12f464aa5674a1abedab0e6_img.png	f717bb64ce704b23b2078f227b2b7345_pdf.pdf
104	Fiji - Lautoka	3	2	3	f9cb2dc1958a43f680ef0ef610ff5496_img.png	4a618ab1ab6c4c2c838665e77a8e9dde_pdf.pdf
105	Fiji - Levuka	3	2	3	57d8b5dc6a8e4cf99190974379908b9b_img.png	4d9413c285184c1ebce7730b9f0e7507_pdf.pdf
106	Fiji - Fiji	3	2	3	03ea5938890b417e97df37056d2b8269_img.png	be63a7ab01f344428d18466519c1b6d6_pdf.pdf
107	Fiji - Malau	3	2	3	0cfbd8c87e47441bbdd4f4bb0f0d78bf_img.png	d0343947e642467d89cc476ebf862d12_pdf.pdf
108	Palau - Koror	13	2	3	5570630329d44348a3efb555ebe496a1_img.png	e9dbeb5dd03f4ac9be025c84e468f7af_pdf.pdf
109	Guam - Guam	6	2	3	3f549789fdf246b7a95275aea96129eb_img.png	ea00c242178145bf891406d39fe91518_pdf.pdf
110	Niue - Niue	10	2	3	37526c92a4994d18a85228758870aa2e_img.png	b2122c5220f145ca82d3337ae98017ba_pdf.pdf
111	Northern Mariana - Saipan	11	2	3	e0590b8eda0a43a6a42bf31b77d04572_img.png	04268845388c4e0a812547376723f98d_pdf.pdf
112	FSM - Kosrae	5	2	3	ea815deda45843bda9c78a150c8eab2f_img.png	cb5b166a822143e19dfcb69b052035d6_pdf.pdf
113	FSM - Chuuk	5	2	3	45ecae28c91243eab8d13a3a0bc60496_img.png	225b7f8b51a24d9cb882fec563ef8002_pdf.pdf
114	FSM - Pohnpei	5	2	3	862140cf745f4e8babf5ce44e41316cb_img.png	da2be78891594661af4627509f9c8781_pdf.pdf
115	FSM - Kapingamarangi	5	2	3	b8717816fb6e46be85fabd67a8ef0544_img.png	624fcb0ae69f48848046eee1daa0e809_pdf.pdf
116	FSM - Ebeye	5	2	3	68828fcd50b34484898a358ed5110eb3_img.png	7aa03260b51f4dc68410c12b1550b3e7_pdf.pdf
117	FSM - Yap	5	2	3	4dbafb6339b241bd93e647692ccc844e_img.png	9cc2bea83570468ab79ba67ddc97d124_pdf.pdf
118	PNG - Rabaul	14	2	3	1de5a5a7d4044643a51d09203c6fb9f8_img.png	6ccebe843e96410c8dcb131f9c0e6690_pdf.pdf
119	PNG - Lae	14	2	3	265f48e37efd45e28e8feee1826b56a6_img.png	0d6858bf9e5b4b7cbc1dc79a741f12f4_pdf.pdf
120	PNG - Vanimo	14	2	3	b9c7a0c63cbf43aa8728c17a33d737f1_img.png	8dade520239c420a8369ea242b12b3ac_pdf.pdf
121	PNG - Bialla	14	2	3	4c8af4473bc7427c9e4684fa155a278f_img.png	8b25813ee4f74b75a68e028eb4049755_pdf.pdf
122	PNG - Samarai	14	2	3	5cbc273bf8884fe3850f35077172a0fc_img.png	27d4a85d9a2e4364a24e4437ac2a0a24_pdf.pdf
123	PNG - Kavieng	14	2	3	ddac5c2f8e204527bb22254567d07263_img.png	901eb1b1921b4b8ca4754abc07e03562_pdf.pdf
124	PNG - Madang	14	2	3	027bd7997d044c66af48dd04601cd5ff_img.png	959461c05105471da57da835282a3d0c_pdf.pdf
125	PNG - Lorengau	14	2	3	d064952344c14690b5ba480b5e962535_img.png	6f43f35eb29b4d91901edced59c4b7fd_pdf.pdf
126	PNG - Arawa	14	2	3	2540ba58f9d24bac892b5e389a8684a6_img.png	ccc9526069cd401d8a60b36d38d0d094_pdf.pdf
127	PNG - Deception	14	2	3	96fbd16ec49345108dffe2e21390f1b0_img.png	eaac99337dd6428791c86a4fd1feb356_pdf.pdf
128	PNG - Kimbe	14	2	3	8a4aa2bbc0f845c0aab667e8d56b122e_img.png	a2f2dca970124cc48de3965d04b9ee92_pdf.pdf
129	PNG - Wewak	14	2	3	f754c4b7efa44c07963997fa4fc93e5b_img.png	e8dbc2a368bc446fbaeb83fbd3e87896_pdf.pdf
130	PNG - IHU	14	2	3	2a789a79b700419d8ac8950d59f3baf4_img.png	7f80d9502388420ea63602159a9f975b_pdf.pdf
131	PNG - Daru	14	2	3	de65f369a1384e5aafe0b71598efce16_img.png	d95feb1db6ee4521af47b55bfa75c6ec_pdf.pdf
132	Solomon Islands - Ghizo	15	2	3	f5da99761cbc46fd9584f695959d2498_img.png	ebc7e2e2a1c046b8a5c62e0595f69b7c_pdf.pdf
133	Solomon Islands - Honiara	15	2	3	80ad1ad0d5c34751b2f4badeba05517d_img.png	03e9353455d04aa185cc5c91fc6f514a_pdf.pdf
134	Solomon Islands - Isabel	15	2	3	07c3041c2084498a9f29c70afe88dc07_img.png	7aec24749f2d4aee945b22d4499fa3ae_pdf.pdf
135	Cook Islands - Avatiu	2	2	3	48fca099c54b45a79e690b8a0e790671_img.png	727b38482cad423eb51f1e77ca63d20b_pdf.pdf
136	Cook Islands - Arutanga	2	2	3	a186355264994659a5a92a9ea42378bb_img.png	486627b118d249b09677e67c8f09a729_pdf.pdf
137	Cook Islands - Penrhyn	2	2	3	15196d6701de4b039aece7f1ebe8d68f_img.png	942d997174634a018103d59f89b25a5f_pdf.pdf
138	Cook Islands - Rarotonga	2	2	3	2701469829a24d72a42b1f4ee1f23005_img.png	bf37ba5a1d21413b8b64591a262fb7e4_pdf.pdf
139	Marshall Islands - Kwajalein	8	2	3	71f313592eef44c98eb799ff14cf39da_img.png	c28b42cd066a4c4fbf53a46c021d80b7_pdf.pdf
140	Marshall Islands - Majuro	8	2	3	4967e1248825494598c8c7513ea56fe5_img.png	eb70671ff2ae42098b4525298515389a_pdf.pdf
141	Nauru - Nauru	9	2	3	2743470443a443d49e2c9793a3e52c46_img.png	58d4093d4ab248b2a57346454daf4d5b_pdf.pdf
142	Noumea - Poindimie	12	2	3	6448c492f600490f854b7bea9a93324c_img.png	483baa7920f145d6b45d148486af00a7_pdf.pdf
143	Noumea - Noumea	12	2	3	1e8d94fc35e54763a1a8910221584bef_img.png	c2e8ad967a2b4a6898164d6ba860e0f2_pdf.pdf
144	Noumea - Mare	12	2	3	0bc38af4f42a43119ecb5eae429e9fd2_img.png	823b90ce89fb49cf8e1ee1280a1ce00b_pdf.pdf
145	Noumea - Thio	12	2	3	a9773ff24f97473a8190de99c00dc53b_img.png	d4b2a21c2827496598e7cd99de3d18e5_pdf.pdf
146	Noumea - Kouaoua	12	2	3	14c04094ad71440badecb5e176b8683b_img.png	098f66e066694e05831130d480bffc03_pdf.pdf
147	Noumea - Poum	12	2	3	fea6ec9b95f246d7bf345ba247722dd8_img.png	ac0782dbc74945dda01a4a01668e5282_pdf.pdf
148	Noumea - Pine	12	2	3	812dfd4b8e3b4168a420f271007e6b42_img.png	d6094419c7f3434bbd13a4207ea5b19c_pdf.pdf
149	Noumea - Nepoui	12	2	3	f2479c5d212a40ab96b17f5cb13459e7_img.png	bec08a4f3b854b00a4a473e31a7bc348_pdf.pdf
150	Vanuatu - Luganville	20	2	3	e5ba01dbfc064789a4b3e2809a1ea3b9_img.png	2483d4422fae4d86bdbfc4dea32df718_pdf.pdf
151	Vanuatu - Port	20	2	3	4516698191194b1fadc2112d35688d9c_img.png	6e286ce276ec4f37a40e9bd22663ebb1_pdf.pdf
152	Vanuatu - Pentecost	20	2	3	12dde1ad50d24668a2136e3ac871a358_img.png	0394a0c59b9744fe86c0d8f7d43e0988_pdf.pdf
153	Vanuatu - Efate	20	2	3	d8000c5d671344d5832c149aa40ab9f8_img.png	f6f5bf6ac7bd4b449b3f0f5c863345e5_pdf.pdf
154	Vanuatu - Aneityum	20	2	3	9580bb26c57a40b7bf701ebb736c6c08_img.png	249d8fea9a0b4ce19e82a1a00aee7346_pdf.pdf
155	Vanuatu - Tanna	20	2	3	e09ba176bd6147b4864d8757ac06c7b3_img.png	c9afdc1b377c4382b254bf04fb92e68e_pdf.pdf
156	Tuvalu - Niulakita	19	2	3	dd349bdf174a42d6a8846ef7ca94cf3f_img.png	cbf449d64c9749a993b9819b01b4b5a3_pdf.pdf
157	Tuvalu - Nanumaga	19	2	3	12237c6196dc488484685d62b4b7a9b8_img.png	6bd267598dad44d696779fc00bcd665c_pdf.pdf
158	Tuvalu - Nukufetau	19	2	3	6e8caa1df9174efdb11d63a459a7b19f_img.png	9b03dcbbd95d43d8b4f3b63e602c3d9f_pdf.pdf
159	Tuvalu - Nanumea	19	2	3	491433cd95634548ba542ad92cec14d1_img.png	bda00a60f8b243f384a40f1db2b89bfe_pdf.pdf
160	Tuvalu - Nui	19	2	3	0a85fff746b74990a9d143362016ddc1_img.png	19ab9028b81044e6b4606239e7b50486_pdf.pdf
161	Tuvalu - Niutao	19	2	3	dd1c21ce42db4bc09094e1a4e16d3e8d_img.png	83eefcdb69954cb4a9f8810381e2e880_pdf.pdf
162	Tuvalu - Vaitupu	19	2	3	1e18985a7b1a462c9755fa8d1c61d1d4_img.png	8a7d3d94b8b144d79426137548760e2e_pdf.pdf
163	Tuvalu - Fongafale	19	2	3	2560fde46ea048f1a7915a960341f66d_img.png	0efb510fac024792a3e88f8d127ef3f1_pdf.pdf
164	Tuvalu - Nukulaelae	19	2	3	bea48b67b201405a91139dc1f8c8cdd0_img.png	da73ad2b89e0493eab75720f7ec2167e_pdf.pdf
165	Tuvalu - Funafuti	19	2	3	905a46a218f942d6828e41e6f6fbc5b3_img.png	0e894db4b8ad495e9356e169eb685ce8_pdf.pdf
166	Tokelau - Nukunonu	17	2	3	2aa6f845bf03415da9448dbdd308eb55_img.png	48fd7f909dba4c89b5d1f258c8dbbc92_pdf.pdf
167	Samoa - Apia	16	2	3	e8279247d0bb4e0f9e676a5443f938ea_img.png	018510c919a94c4686670d6aca9449ed_pdf.pdf
168	Cook Islands - Survey Report	2	3	4	47119672ac074e2db05197f20f258004_img.png	8eac3f9c01cb4aa790d388a06a8e8e7a_pdf.pdf
169	Fiji - Survey Report	3	3	4	8e8d65274d7c44c5ba2aac72922cdddf_img.png	dbfc3c4b8b814ccd8d7c0508e25c91cf_pdf.pdf
170	FSM - Survey Report	5	3	4	f1ddf61b7efe4162a8bc288ad2a1fcbc_img.png	3555286ae32d46ff9d2e6b2dc0e2923b_pdf.pdf
171	MHL - Survey Report	8	3	4	04de35749d0c42238deb61f8e662d195_img.png	b9dcb822003e4065bc8482b4631e09b8_pdf.pdf
172	NRU - Survey Report	9	3	4	dc113c15423c4bb8bbfcf601848f73ff_img.png	b73818bc3fec4df884d1273245a896f2_pdf.pdf
173	PNG - Survey Report	14	3	4	40be0fafe9dc492fb4673c8e2bc11581_img.png	7b2ad3c064e8454bbec6614217b06c4c_pdf.pdf
174	SB - Survey Report	15	3	4	803ad6c30bca4570aebdbab895b6d07e_img.png	d8f4ffe7a395459bab316853a8a9c6d2_pdf.pdf
175	TO - Survey Report	18	3	4	1c7c8b344ce847b686a645cdf4212ea3_img.png	7de0234bc6114ae89b592d8dcbc902c6_pdf.pdf
176	TV - Survey Report	19	3	4	d6761fe76d984b92852e8b6d905fa071_img.png	bc26a993ebd1403aa05ae404c8770252_pdf.pdf
177	VU - Survey Report	20	3	4	10c13a2b06084ad8a7271613bcb5fbdb_img.png	1ca6fa44a2034a018708553ec7e3deaf_pdf.pdf
178	WS - Survey Report	16	3	4	0b31d676c7ae4e43a284fcfb1d825048_img.png	7e1ec320f69b4b5593f85acfbb62912e_pdf.pdf
\.


--
-- Data for Name: years; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.years (id, value, name) FROM stdin;
1	2025	2025
2	2024	2024
3	2023	2023
4	2019	2019
\.


--
-- Name: countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.countries_id_seq', 21, true);


--
-- Name: document_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.document_types_id_seq', 3, true);


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_id_seq', 178, true);


--
-- Name: years_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.years_id_seq', 4, true);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: document_types document_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_types
    ADD CONSTRAINT document_types_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: years years_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.years
    ADD CONSTRAINT years_pkey PRIMARY KEY (id);


--
-- Name: ix_countries_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_countries_id ON public.countries USING btree (id);


--
-- Name: ix_countries_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_countries_name ON public.countries USING btree (name);


--
-- Name: ix_countries_value; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_countries_value ON public.countries USING btree (value);


--
-- Name: ix_document_types_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_document_types_id ON public.document_types USING btree (id);


--
-- Name: ix_document_types_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_document_types_name ON public.document_types USING btree (name);


--
-- Name: ix_document_types_value; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_document_types_value ON public.document_types USING btree (value);


--
-- Name: ix_documents_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_documents_id ON public.documents USING btree (id);


--
-- Name: ix_documents_title; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_documents_title ON public.documents USING btree (title);


--
-- Name: ix_years_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_years_id ON public.years USING btree (id);


--
-- Name: ix_years_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_years_name ON public.years USING btree (name);


--
-- Name: ix_years_value; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_years_value ON public.years USING btree (value);


--
-- Name: documents documents_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.countries(id);


--
-- Name: documents documents_document_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_document_type_id_fkey FOREIGN KEY (document_type_id) REFERENCES public.document_types(id);


--
-- Name: documents documents_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_year_id_fkey FOREIGN KEY (year_id) REFERENCES public.years(id);


--
-- PostgreSQL database dump complete
--

