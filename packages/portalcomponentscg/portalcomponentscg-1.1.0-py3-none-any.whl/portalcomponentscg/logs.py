# import logging
#
# from portalcomponentscg import const
# from portalcomponentscg.requests_cg import post_cg, Requests
#
# logging.basicConfig(filename='logsPortal.log', level=logging.INFO,
#                     format='%(levelname)s - %(message)s')
#
#
# class LogsMicroService(object):
#
#     def __init__(self, microservice: str = None, info_messages: str = None, error_messages: str = None,
#                  success_messages: str = None, critical_messages: str = None):
#
#         self.microservice = microservice
#         self.info_messages = info_messages
#         self.error_messages = error_messages
#         self.success_messages = success_messages
#         self.critical_messages = critical_messages
#
#     def LogsMicroService(self):
#         json = {'microservice': self.microservice}
#
#         Requests()
#         teste = Requests('http://127.0.0.1:8000/rest-auth/login/', 'nunes', '1611',
#                          url_request='http://127.0.0.1:8000/api/v1/empresas').get_cg()
#         post_cg(const.URL_API_MICROSERVICE, json)
#
#
# def LogsInfo(messages):
#
#     json = {
#         "info_message": [
#             {
#                 "messages": messages
#             }
#         ]
#     }
#     post_cg(const.URL_API_INFOS, json)
#
#     logging.info(messages)
#     pass
#
#
# def LogsErros(erros):
#
#     json = {
#         #"traceback": traceback,
#         "error_mesage": erros
#     }
#     post_cg(const.URL_API_ERROS, json)
#
#     logging.error(erros)
#     pass
#
#
# def LogsCriticalErros(critical):
#
#     json = {
#             "critical": critical
#     }
#     post_cg(const.URL_API_CRITICALS, json)
#
#     logging.warning(critical)
#     pass
#
#
# def LogsSuccess(success):
#
#     json = {
#         "success_mesage": success
#     }
#     post_cg(const.URL_API_SUCCESS, json)
#
#     logging.info(success)
#     pass