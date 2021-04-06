echo "Starting #corona"
python Exporter.py --querysearch "#corona" --since 2020-04-03 --until 2020-04-06 --output "#corona.csv"
echo "Finishing #corona"

echo "Starting #quarantine"
python Exporter.py --querysearch "#quarantine" --since 2020-04-03 --until 2020-04-06 --output "#quarantine.csv"
echo "Finishing #quarantine"

echo "Starting #karantina"
python Exporter.py --querysearch "#karantina" --since 2020-04-03 --until 2020-04-06 --output "#karantina.csv"
echo "Finishing #karantina"

echo "Starting #covid19"
python Exporter.py --querysearch "#covid19" --since 2020-04-03 --until 2020-04-06 --output "#covid19.csv"
echo "Finishing #covid19"

