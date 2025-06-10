SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: generate_hub_account_hk_account_id(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_hub_account_hk_account_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hk_account_id := sha256(NEW.account_number);
 RETURN NEW;
END
$$;


--
-- Name: generate_hub_customer_hk_customer_id(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_hub_customer_hk_customer_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hk_customer_id := sha256(NEW.customer_id);
 RETURN NEW;
END
$$;


--
-- Name: generate_hub_product_hk_product_id(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_hub_product_hk_product_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hk_product_id := sha256(NEW.product_id);
 RETURN NEW;
END
$$;


--
-- Name: generate_hub_transaction_hk_transaction_id(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_hub_transaction_hk_transaction_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hk_transaction_id := sha256(NEW.transaction_id);
 RETURN NEW;
END
$$;


--
-- Name: generate_link_account_product_hk_link_account_product_id(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_link_account_product_hk_link_account_product_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hk_link_account_product_id := sha256(
	concat(NEW.hk_account_id, '|', NEW.hk_product_id, '|', NEW.load_dts)
 );
 RETURN NEW;
END
$$;


--
-- Name: generate_link_account_transaction_hk_link_account_transaction_i(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_link_account_transaction_hk_link_account_transaction_i() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hk_link_account_transaction_id := sha256(
	concat(NEW.hk_account_id, '|', NEW.hk_transaction_id, '|', NEW.load_dts)
 );
 RETURN NEW;
END
$$;


--
-- Name: generate_link_customer_account_hk_link_customer_account_id(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_link_customer_account_hk_link_customer_account_id() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hk_link_customer_account_id := sha256(
	concat(NEW.hk_customer_id, '|', NEW.hk_account_id, '|', NEW.load_dts)
 );
 RETURN NEW;
END
$$;


--
-- Name: generate_sat_account_details_hash_diff(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_sat_account_details_hash_diff() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hash_diff := sha256(
	concat(
	'|', NEW.open_date, 
	'|', NEW.close_date,
	'|', NEW.status,
	'|', NEW.balance,
	'|', NEW.currency
	)
 );
 RETURN NEW;
END
$$;


--
-- Name: generate_sat_customer_details_hash_diff(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_sat_customer_details_hash_diff() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hash_diff := sha256(
	concat(
	'|', NEW.first_name, 
	'|', NEW.last_name,
	'|', NEW.birth_date,
	'|', NEW.tax_id,
	'|', NEW.phone_number,
	'|', NEW.email,
	'|', NEW.address
	)
 );
 RETURN NEW;
END
$$;


--
-- Name: generate_sat_product_details_hash_diff(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_sat_product_details_hash_diff() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hash_diff := sha256(
	concat(
	'|', NEW.product_name, 
	'|', NEW.product_type,
	'|', NEW.interest_rate,
	'|', NEW.term
	)
 );
 RETURN NEW;
END
$$;


--
-- Name: generate_sat_transaction_details_hash_diff(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_sat_transaction_details_hash_diff() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 NEW.hash_diff := sha256(
	concat(
	'|', NEW.transaction_date, 
	'|', NEW.amount,
	'|', NEW.description,
	'|', NEW.transaction_type
	)
 );
 RETURN NEW;
END
$$;


--
-- Name: sha256(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.sha256(text) RETURNS text
    LANGUAGE plpgsql IMMUTABLE
    AS $_$
BEGIN
    RETURN encode(digest($1, 'sha256'), 'hex');
END;
$_$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: hub_account; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hub_account (
    hk_account_id text NOT NULL,
    account_number text NOT NULL,
    load_ts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    record_source text
);


--
-- Name: hub_customer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hub_customer (
    hk_customer_id text NOT NULL,
    customer_id text NOT NULL,
    load_ts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    record_source text
);


--
-- Name: hub_product; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hub_product (
    hk_product_id text NOT NULL,
    product_code text NOT NULL,
    load_dts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    record_source text
);


--
-- Name: hub_transaction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hub_transaction (
    hk_transaction_id text NOT NULL,
    transaction_id text NOT NULL,
    load_dts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    record_source text
);


--
-- Name: link_account_product; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.link_account_product (
    hk_link_account_product_id text NOT NULL,
    hk_account_id text NOT NULL,
    hk_product_id text NOT NULL,
    load_dts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    record_source text
);


--
-- Name: link_account_transaction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.link_account_transaction (
    hk_link_account_transaction_id text NOT NULL,
    hk_account_id text NOT NULL,
    load_dts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    record_source text,
    hk_transaction_id text NOT NULL
);


--
-- Name: link_customer_account; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.link_customer_account (
    hk_link_customer_account_id text NOT NULL,
    hk_customer_id text NOT NULL,
    hk_account_id text NOT NULL,
    load_dts timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    record_source text
);


--
-- Name: sat_account_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sat_account_details (
    hk_account_id text NOT NULL,
    load_dts timestamp with time zone NOT NULL,
    open_date date,
    close_date date,
    status text,
    balance numeric,
    currency text,
    hash_diff text NOT NULL,
    record_source text NOT NULL
);


--
-- Name: sat_customer_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sat_customer_details (
    hk_customer_id text NOT NULL,
    load_dts timestamp with time zone NOT NULL,
    first_name text,
    last_name text,
    birth_date date,
    tax_id text,
    phone_number text,
    email text,
    address text,
    hash_diff text NOT NULL,
    record_source text NOT NULL
);


--
-- Name: sat_product_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sat_product_details (
    hk_product_id text NOT NULL,
    load_dts timestamp with time zone NOT NULL,
    product_name text,
    product_type text,
    interest_rate numeric,
    term integer,
    hash_diff text NOT NULL,
    record_source text NOT NULL
);


--
-- Name: sat_transaction_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sat_transaction_details (
    hk_transaction_id text NOT NULL,
    load_dts timestamp with time zone,
    transaction_date timestamp with time zone,
    amount numeric,
    description text,
    transaction_type text,
    hash_diff text,
    record_source text
);


--
-- Name: hub_account hub_account_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hub_account
    ADD CONSTRAINT hub_account_pkey PRIMARY KEY (hk_account_id);


--
-- Name: hub_customer hub_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hub_customer
    ADD CONSTRAINT hub_customer_pkey PRIMARY KEY (hk_customer_id);


--
-- Name: hub_product hub_product_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hub_product
    ADD CONSTRAINT hub_product_pkey PRIMARY KEY (hk_product_id);


--
-- Name: hub_transaction hub_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hub_transaction
    ADD CONSTRAINT hub_transaction_pkey PRIMARY KEY (hk_transaction_id);


--
-- Name: link_account_product link_account_product_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_account_product
    ADD CONSTRAINT link_account_product_pkey PRIMARY KEY (hk_link_account_product_id);


--
-- Name: link_account_transaction link_account_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_account_transaction
    ADD CONSTRAINT link_account_transaction_pkey PRIMARY KEY (hk_link_account_transaction_id);


--
-- Name: link_customer_account link_customer_account_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_customer_account
    ADD CONSTRAINT link_customer_account_pkey PRIMARY KEY (hk_link_customer_account_id);


--
-- Name: sat_account_details sat_account_details_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_account_details
    ADD CONSTRAINT sat_account_details_pkey PRIMARY KEY (hk_account_id, load_dts);


--
-- Name: sat_customer_details sat_customer_details_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_customer_details
    ADD CONSTRAINT sat_customer_details_pkey PRIMARY KEY (hk_customer_id, load_dts);


--
-- Name: sat_product_details sat_product_details_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_product_details
    ADD CONSTRAINT sat_product_details_pkey PRIMARY KEY (hk_product_id, load_dts);


--
-- Name: sat_transaction_details sat_transaction_details_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_transaction_details
    ADD CONSTRAINT sat_transaction_details_pkey PRIMARY KEY (hk_transaction_id);


--
-- Name: hub_account trg_generate_hub_account_hk_account_id; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_hub_account_hk_account_id BEFORE INSERT ON public.hub_account FOR EACH ROW EXECUTE FUNCTION public.generate_hub_account_hk_account_id();


--
-- Name: hub_customer trg_generate_hub_customer_hk_customer_id; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_hub_customer_hk_customer_id BEFORE INSERT ON public.hub_customer FOR EACH ROW EXECUTE FUNCTION public.generate_hub_customer_hk_customer_id();


--
-- Name: hub_product trg_generate_hub_product_hk_product_id; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_hub_product_hk_product_id BEFORE INSERT ON public.hub_product FOR EACH ROW EXECUTE FUNCTION public.generate_hub_product_hk_product_id();


--
-- Name: hub_transaction trg_generate_hub_transaction_hk_transaction_id; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_hub_transaction_hk_transaction_id BEFORE INSERT ON public.hub_transaction FOR EACH ROW EXECUTE FUNCTION public.generate_hub_transaction_hk_transaction_id();


--
-- Name: link_account_product trg_generate_link_account_product_hk_link_account_product_id; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_link_account_product_hk_link_account_product_id BEFORE INSERT ON public.link_account_product FOR EACH ROW EXECUTE FUNCTION public.generate_link_account_product_hk_link_account_product_id();


--
-- Name: link_account_transaction trg_generate_link_account_transaction_hk_link_account_transacti; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_link_account_transaction_hk_link_account_transacti BEFORE INSERT ON public.link_account_transaction FOR EACH ROW EXECUTE FUNCTION public.generate_link_account_transaction_hk_link_account_transaction_i();


--
-- Name: link_customer_account trg_generate_link_customer_account_hk_link_customer_account_id; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_link_customer_account_hk_link_customer_account_id BEFORE INSERT ON public.link_customer_account FOR EACH ROW EXECUTE FUNCTION public.generate_link_customer_account_hk_link_customer_account_id();


--
-- Name: sat_account_details trg_generate_sat_account_details_hash_diff; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_sat_account_details_hash_diff BEFORE INSERT ON public.sat_account_details FOR EACH ROW EXECUTE FUNCTION public.generate_sat_account_details_hash_diff();


--
-- Name: sat_customer_details trg_generate_sat_customer_details_hash_diff; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_sat_customer_details_hash_diff BEFORE INSERT ON public.sat_customer_details FOR EACH ROW EXECUTE FUNCTION public.generate_sat_customer_details_hash_diff();


--
-- Name: sat_product_details trg_generate_sat_product_details_hash_diff; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_sat_product_details_hash_diff BEFORE INSERT ON public.sat_product_details FOR EACH ROW EXECUTE FUNCTION public.generate_sat_product_details_hash_diff();


--
-- Name: sat_transaction_details trg_generate_sat_transaction_details_hash_diff; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER trg_generate_sat_transaction_details_hash_diff BEFORE INSERT ON public.sat_transaction_details FOR EACH ROW EXECUTE FUNCTION public.generate_sat_transaction_details_hash_diff();


--
-- Name: link_account_transaction fk_hk_account_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_account_transaction
    ADD CONSTRAINT fk_hk_account_id FOREIGN KEY (hk_account_id) REFERENCES public.hub_account(hk_account_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: link_customer_account fk_hk_account_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_customer_account
    ADD CONSTRAINT fk_hk_account_id FOREIGN KEY (hk_account_id) REFERENCES public.hub_account(hk_account_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sat_account_details fk_hk_account_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_account_details
    ADD CONSTRAINT fk_hk_account_id FOREIGN KEY (hk_account_id) REFERENCES public.hub_account(hk_account_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: link_account_product fk_hk_account_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_account_product
    ADD CONSTRAINT fk_hk_account_id FOREIGN KEY (hk_account_id) REFERENCES public.hub_account(hk_account_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: link_customer_account fk_hk_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_customer_account
    ADD CONSTRAINT fk_hk_customer_id FOREIGN KEY (hk_customer_id) REFERENCES public.hub_customer(hk_customer_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sat_customer_details fk_hk_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_customer_details
    ADD CONSTRAINT fk_hk_customer_id FOREIGN KEY (hk_customer_id) REFERENCES public.hub_customer(hk_customer_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sat_product_details fk_hk_product_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_product_details
    ADD CONSTRAINT fk_hk_product_id FOREIGN KEY (hk_product_id) REFERENCES public.hub_product(hk_product_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: link_account_product fk_hk_product_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_account_product
    ADD CONSTRAINT fk_hk_product_id FOREIGN KEY (hk_product_id) REFERENCES public.hub_product(hk_product_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: link_account_transaction fk_hk_transaction_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.link_account_transaction
    ADD CONSTRAINT fk_hk_transaction_id FOREIGN KEY (hk_transaction_id) REFERENCES public.hub_transaction(hk_transaction_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sat_transaction_details sat_transaction_details_hk_transaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sat_transaction_details
    ADD CONSTRAINT sat_transaction_details_hk_transaction_id_fkey FOREIGN KEY (hk_transaction_id) REFERENCES public.hub_transaction(hk_transaction_id);


--
-- PostgreSQL database dump complete
--

