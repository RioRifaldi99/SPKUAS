PGDMP                         {         
   smartphone    14.9    14.9     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16394 
   smartphone    DATABASE     j   CREATE DATABASE smartphone WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_Indonesia.1252';
    DROP DATABASE smartphone;
                postgres    false            �            1259    16395 	   handphone    TABLE     J  CREATE TABLE public.handphone (
    id integer NOT NULL,
    nama_handphone character varying(255) NOT NULL,
    "ram_Gb" integer NOT NULL,
    "rom_Gb" integer NOT NULL,
    chipset character varying(255) NOT NULL,
    layar character varying(255) NOT NULL,
    "harga_Rp" integer NOT NULL,
    "baterai_mAh" integer NOT NULL
);
    DROP TABLE public.handphone;
       public         heap    postgres    false            �            1259    16398    handphone_id_seq    SEQUENCE     �   CREATE SEQUENCE public.handphone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.handphone_id_seq;
       public          postgres    false    209            �           0    0    handphone_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.handphone_id_seq OWNED BY public.handphone.id;
          public          postgres    false    210            \           2604    16399    handphone id    DEFAULT     l   ALTER TABLE ONLY public.handphone ALTER COLUMN id SET DEFAULT nextval('public.handphone_id_seq'::regclass);
 ;   ALTER TABLE public.handphone ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    210    209            �          0    16395 	   handphone 
   TABLE DATA           v   COPY public.handphone (id, nama_handphone, "ram_Gb", "rom_Gb", chipset, layar, "harga_Rp", "baterai_mAh") FROM stdin;
    public          postgres    false    209   �       �           0    0    handphone_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.handphone_id_seq', 10, true);
          public          postgres    false    210            ^           2606    16406    handphone handphone_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.handphone
    ADD CONSTRAINT handphone_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.handphone DROP CONSTRAINT handphone_pkey;
       public            postgres    false    209            �     x���MN�0FדS�	"�$����hPSHl�� +�5���A�hx1��o�y>
/F���F�|�� �I��Ψ�nq�;�p�Rq��6���D6Zu���?I@$WhF�QqB9Ԫ?��T���X8����"����i0:�g����v���'i6��u
�ఠ��yh�8���wc��� &����ۡv[�X����-�e�<.�-�޵Fa�ə|�ft�e.����W��Ρr�w����J���aС6%p�����|Q�����z��(�-���     